import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import GlassCard from '../components/GlassCard';

const ScheduleMaker = () => {
  const [availableTime, setAvailableTime] = useState('');
  const [resources, setResources] = useState(['']);
  const [schedule, setSchedule] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Time options in minutes
  const timeOptions = [
    { value: 15, label: '15 minutes' },
    { value: 30, label: '30 minutes' },
    { value: 60, label: '1 hour' },
    { value: 90, label: '1.5 hours' },
    { value: 120, label: '2 hours' },
    { value: 180, label: '3 hours' },
    { value: 240, label: '4 hours' },
    { value: 300, label: '5 hours' },
    { value: 360, label: '6 hours' },
    { value: 420, label: '7 hours' },
    { value: 480, label: '8 hours' },
    { value: 540, label: '9 hours' },
    { value: 600, label: '10 hours' },
    { value: 660, label: '11 hours' },
    { value: 720, label: '12 hours' }
  ];

  const addResource = () => {
    setResources([...resources, '']);
  };

  const updateResource = (index, value) => {
    const newResources = [...resources];
    newResources[index] = value;
    setResources(newResources);
  };

  const removeResource = (index) => {
    if (resources.length > 1) {
      const newResources = resources.filter((_, i) => i !== index);
      setResources(newResources);
    }
  };

  const generateSchedule = async () => {
    try {
      setIsLoading(true);
      
      // Check if we have YouTube URL input
      const youtubeUrl = document.getElementById('youtube-url')?.value;
      const duration = document.getElementById('duration')?.value;
      
      if (youtubeUrl) {
        // Generate YouTube video schedule
        await generateYouTubeSchedule(youtubeUrl, duration);
      } else {
        // Generate regular ML schedule
        await generateMLSchedule();
      }
    } catch (e) {
      console.error(e);
      alert('Failed to generate schedule.');
    } finally {
      setIsLoading(false);
    }
  };

  const generateYouTubeSchedule = async (youtubeUrl, duration) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/schedules/generate-youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          youtube_url: youtubeUrl,
          duration_hours: parseFloat(duration) || 3.0,
          title: 'My YouTube Learning Schedule'
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate YouTube schedule');
      }
      
      const result = await response.json();
      const items = result.data.schedule_items || [];
      
      // Map to frontend format with proper timing and learning topics
      const mapped = items.map((item, idx) => ({
        day: item.day_of_week,
        start_time: item.start_time,
        end_time: item.end_time,
        hours: item.estimated_hours,
        topics: item.resource_title,
        learning_topic: item.learning_topic || item.resource_title,
        learning_objectives: item.learning_objectives || [],
        key_concepts: item.key_concepts || [],
        video_url: item.video_url,
        session_number: item.session_number,
        break_after: item.break_after || 0
      }));
      
      setSchedule(mapped);
      alert(`YouTube schedule generated! ${result.data.video_info.sessions_count} sessions created.`);
      
    } catch (e) {
      console.error('YouTube schedule error:', e);
      throw e;
    }
  };

  const generateMLSchedule = async () => {
    try {
      // Fetch goals
      const goalsRes = await fetch('http://localhost:8000/api/v1/learning/goals');
      const goalsJson = await goalsRes.json();
      const goalIds = (goalsJson?.data || []).map(g => g.id);
      if (!goalIds.length) {
        alert('Please create at least one learning goal first.');
        return;
      }
      
      // Generate schedule for next month window (placeholder dates)
      const genRes = await fetch('http://localhost:8000/api/v1/schedules/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          goal_ids: goalIds,
          start_date: '2025-01-15',
          end_date: '2025-02-15',
          title: 'My Learning Schedule'
        })
      });
      
      if (!genRes.ok) {
        const txt = await genRes.text();
        throw new Error(txt);
      }
      
      const genJson = await genRes.json();
      const items = genJson?.data?.schedule_items || [];
      const mapped = items.map((it, idx) => ({
        day: it.day_of_week,
        hours: it.estimated_hours,
        topics: it.resource_title
      }));
      
      setSchedule(mapped);
      
    } catch (e) {
      console.error('ML schedule error:', e);
      throw e;
    }
  };

  const copyTableToClipboard = () => {
    const tableText = schedule.map(row => 
      `${row.day}\t${row.start_time} - ${row.end_time}\t${row.hours}h\t${row.topics}\t${row.break_after > 0 ? `${row.break_after}min break` : 'No break'}`
    ).join('\n');
    
    const header = 'Day\tTime\tDuration\tSession\tBreak\n';
    const fullText = header + tableText;
    
    navigator.clipboard.writeText(fullText);
    alert('Schedule copied to clipboard with timing information!');
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="min-h-screen py-12"
    >
      <div className="container mx-auto px-4">
        <GlassCard className="p-8 max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-[#330033] mb-8 text-center">
            Create Your Learning Schedule
          </h1>

          <div className="space-y-6">
            {/* Time Picker Section */}
            <div>
              <label className="block text-[#330033] font-semibold mb-4">
                Available Time Per Day
              </label>
              <div className="time-picker-container">
                <div className="time-picker-scroll">
                  {timeOptions.map((time) => (
                    <motion.button
                      key={time.value}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setAvailableTime(time.value)}
                      className={`time-option ${availableTime === time.value ? 'time-option-active' : ''}`}
                    >
                      <span className="time-value">{time.label}</span>
                      {availableTime === time.value && (
                        <motion.div 
                          className="time-selection-indicator"
                          layoutId="timeSelection"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ type: "spring", stiffness: 500, damping: 30 }}
                        />
                      )}
                    </motion.button>
                  ))}
                </div>
                <div className="time-picker-gradient-top"></div>
                <div className="time-picker-gradient-bottom"></div>
              </div>
              {availableTime && (
                <motion.p 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-[#330033] text-sm mt-3 text-center"
                >
                  Selected: {timeOptions.find(t => t.value === availableTime)?.label}
                </motion.p>
              )}
            </div>

            {/* YouTube Video Section */}
            <div>
              <label className="block text-[#330033] font-semibold mb-2">
                YouTube Video (NEW!)
              </label>
              <div className="space-y-3">
                <input
                  id="youtube-url"
                  type="text"
                  className="w-full p-3 rounded-lg border border-[#330033] bg-transparent text-[#330033]"
                  placeholder="Paste YouTube URL here..."
                />
                <div className="flex space-x-2">
                  <input
                    id="duration"
                    type="number"
                    step="0.5"
                    min="0.5"
                    max="20"
                    defaultValue="3.0"
                    className="flex-1 p-3 rounded-lg border border-[#330033] bg-transparent text-[#330033]"
                    placeholder="Duration (hours)"
                  />
                  <span className="flex items-center text-[#330033] font-medium">hours</span>
                </div>
                <p className="text-sm text-[#330033] opacity-70">
                  ✨ AI will automatically break down your video into smart learning sessions!
                </p>
              </div>
            </div>

            {/* Resources Section (Fallback) */}
            <div>
              <label className="block text-[#330033] font-semibold mb-2">
                Other Learning Resources (Optional)
              </label>
              {resources.map((resource, index) => (
                <div key={index} className="flex space-x-2 mb-2">
                  <input
                    type="text"
                    value={resource}
                    onChange={(e) => updateResource(index, e.target.value)}
                    className="flex-1 p-3 rounded-lg border border-[#330033] bg-transparent text-[#330033]"
                    placeholder="PDF link, document URL, etc..."
                  />
                  {resources.length > 1 && (
                    <button
                      onClick={() => removeResource(index)}
                      className="btn-primary px-4"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                onClick={addResource}
                className="btn-primary mt-2"
              >
                Add Another Resource
              </button>
            </div>

            <button
              onClick={generateSchedule}
              disabled={isLoading || !availableTime}
              className="btn-primary w-full py-4 text-lg"
            >
              {isLoading ? 'Generating Schedule...' : 'Go!'}
            </button>
          </div>

          <AnimatePresence>
            {schedule && (
              <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-12"
              >
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-[#330033]">
                    Your Learning Schedule
                  </h2>
                  <button
                    onClick={copyTableToClipboard}
                    className="btn-primary"
                  >
                    Copy Schedule
                  </button>
                </div>

                <GlassCard className="p-6">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-[#330033]">
                        <th className="text-left p-3 text-[#330033] font-semibold">Day</th>
                        <th className="text-left p-3 text-[#330033] font-semibold">Time</th>
                        <th className="text-left p-3 text-[#330033] font-semibold">Duration</th>
                        <th className="text-left p-3 text-[#330033] font-semibold">Session</th>
                        <th className="text-left p-3 text-[#330033] font-semibold">Break</th>
                      </tr>
                    </thead>
                    <tbody>
                      <AnimatePresence>
                        {schedule.map((row, index) => (
                          <motion.tr
                            key={index}
                            initial={{ opacity: 0, x: -50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.2 }}
                            className="border-b border-[#330033] border-opacity-30 hover:bg-[#330033] hover:bg-opacity-5"
                          >
                            <td className="p-3 text-[#330033] font-medium capitalize">{row.day}</td>
                            <td className="p-3 text-[#330033]">
                              <div className="flex items-center space-x-2">
                                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm font-mono">
                                  {row.start_time}
                                </span>
                                <span className="text-gray-400">→</span>
                                <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm font-mono">
                                  {row.end_time}
                                </span>
                              </div>
                            </td>
                            <td className="p-3 text-[#330033]">
                              <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-sm font-medium">
                                {row.hours}h
                              </span>
                            </td>
                            <td className="p-3 text-[#330033]">
                              <div className="max-w-xs">
                                <div className="font-medium text-sm text-[#330033] mb-1">
                                  {row.learning_topic}
                                </div>
                                {row.learning_objectives && row.learning_objectives.length > 0 && (
                                  <div className="text-xs text-[#330033] opacity-80 mb-1">
                                    <div className="font-semibold">Objectives:</div>
                                    <ul className="list-disc list-inside ml-2">
                                      {row.learning_objectives.slice(0, 2).map((obj, idx) => (
                                        <li key={idx}>{obj}</li>
                                      ))}
                                    </ul>
                                  </div>
                                )}
                                {row.key_concepts && row.key_concepts.length > 0 && (
                                  <div className="text-xs text-[#330033] opacity-70 mb-2">
                                    <div className="font-semibold">Key Concepts:</div>
                                    <div className="flex flex-wrap gap-1 mt-1">
                                      {row.key_concepts.slice(0, 3).map((concept, idx) => (
                                        <span key={idx} className="bg-blue-100 text-blue-800 px-1 py-0.5 rounded text-xs">
                                          {concept}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}
                                {row.video_url && (
                                  <a 
                                    href={row.video_url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:text-blue-800 text-xs underline"
                                  >
                                    Watch Video
                                  </a>
                                )}
                              </div>
                            </td>
                            <td className="p-3 text-[#330033]">
                              {row.break_after > 0 ? (
                                <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded text-sm">
                                  {row.break_after}min
                                </span>
                              ) : (
                                <span className="text-gray-400 text-sm">-</span>
                              )}
                            </td>
                          </motion.tr>
                        ))}
                      </AnimatePresence>
                    </tbody>
                  </table>
                </GlassCard>
              </motion.div>
            )}
          </AnimatePresence>
        </GlassCard>
      </div>
    </motion.div>
  );
};

export default ScheduleMaker;