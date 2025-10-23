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

  const generateSchedule = () => {
    setIsLoading(true);
    
    // Mock schedule generation
    setTimeout(() => {
      const mockSchedule = [
        { day: 'Day 1', hours: 4, topics: 'Introduction to React & Components' },
        { day: 'Day 2', hours: 5, topics: 'State Management & Hooks' },
        { day: 'Day 3', hours: 6, topics: 'Routing & API Integration' },
        { day: 'Day 4', hours: 4, topics: 'Project Implementation' },
      ];
      setSchedule(mockSchedule);
      setIsLoading(false);
    }, 2000);
  };

  const copyTableToClipboard = () => {
    const tableText = schedule.map(row => 
      `${row.day}\t${row.hours} hours\t${row.topics}`
    ).join('\n');
    
    navigator.clipboard.writeText(tableText);
    alert('Schedule copied to clipboard!');
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

            {/* Resources Section (Unchanged) */}
            <div>
              <label className="block text-[#330033] font-semibold mb-2">
                Learning Resources
              </label>
              {resources.map((resource, index) => (
                <div key={index} className="flex space-x-2 mb-2">
                  <input
                    type="text"
                    value={resource}
                    onChange={(e) => updateResource(index, e.target.value)}
                    className="flex-1 p-3 rounded-lg border border-[#330033] bg-transparent text-[#330033]"
                    placeholder="Paste YouTube URL, PDF link, document URL..."
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
                        <th className="text-left p-3 text-[#330033] font-semibold">Hours</th>
                        <th className="text-left p-3 text-[#330033] font-semibold">Topics</th>
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
                            className="border-b border-[#330033] border-opacity-30"
                          >
                            <td className="p-3 text-[#330033]">{row.day}</td>
                            <td className="p-3 text-[#330033]">{row.hours} hours</td>
                            <td className="p-3 text-[#330033]">{row.topics}</td>
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