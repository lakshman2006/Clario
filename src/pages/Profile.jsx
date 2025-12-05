import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { authenticatedRequest, isAuthenticated, removeToken } from '../utils/auth';
import GlassCard from '../components/GlassCard';

// Import icons (you can use react-icons library or your own icon components)
// If using react-icons: npm install react-icons
import { 
  FaUser, 
  FaBook, 
  FaCog, 
  FaCalendar,
  FaClock,
  FaBookOpen,
  FaTrash,
  FaEye,
  FaPlay,
  FaCheckCircle,
  FaEnvelope,
  FaChartLine,
  FaBell,
  FaGlobe,
  FaPalette
} from 'react-icons/fa';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [savedSchedules, setSavedSchedules] = useState([]);
  const [activeTab, setActiveTab] = useState('profile');
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch user profile data from backend
  const fetchUserProfile = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/users/profile', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch profile');
      }

      const userData = await response.json();
      setUser(userData.data);
    } catch (err) {
      setError('Failed to load profile data');
      console.error('Error fetching user profile:', err);
      if (err.message.includes('Not authenticated') || err.message.includes('401')) {
        window.location.href = '/login';
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch user's saved schedules from backend
  const fetchUserSchedules = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/schedules/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch schedules');
      }

      const schedulesData = await response.json();
      setSavedSchedules(schedulesData.data || []);
    } catch (err) {
      console.error('Error fetching schedules:', err);
      setSavedSchedules([]);
    }
  };

  // Update user profile
  const updateUserProfile = async (updatedData) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/users/profile', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const updatedUser = await response.json();
      setUser(updatedUser);
      return updatedUser;
    } catch (err) {
      throw new Error('Failed to update profile');
    }
  };

  // Delete a schedule
  const deleteSchedule = async (scheduleId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/schedules/${scheduleId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete schedule');
      }

      setSavedSchedules(prev => prev.filter(schedule => schedule.id !== scheduleId));
    } catch (err) {
      console.error('Error deleting schedule:', err);
      alert('Failed to delete schedule');
    }
  };

  // Load data on component mount
  // Check authentication on component mount
  useEffect(() => {
    if (!isAuthenticated()) {
      window.location.href = '/login';
      return;
    }
    fetchUserProfile();
    fetchUserSchedules();
  }, []);

  const handleLogout = async () => {
    try {
      // Call backend logout endpoint
      const token = localStorage.getItem('access_token');
      if (token) {
        await fetch('http://localhost:8000/api/v1/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always remove token and redirect
      removeToken();
      window.location.href = '/login';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="loading-spinner-large"></div>
      </div>
    );
  }

  if (error && !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <GlassCard className="p-8 text-center">
          <h2 className="text-2xl font-bold text-[#330033] mb-4">Error Loading Profile</h2>
          <p className="text-[#330033] opacity-80 mb-4">{error}</p>
          <button 
            onClick={fetchUserProfile}
            className="btn-primary"
          >
            Try Again
          </button>
        </GlassCard>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="min-h-screen py-12"
    >
      <div className="container">
        <div className="profile-header">
          <div>
            <h1 className="profile-main-title">Your Profile</h1>
            <p className="profile-subtitle">Manage your account and view your learning history</p>
          </div>
          <button 
            onClick={handleLogout}
            className="logout-btn"
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#ff6b6b',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              cursor: 'pointer',
              fontSize: '0.9rem'
            }}
          >
            Logout
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="error-message"
          >
            {error}
          </motion.div>
        )}

        {/* Tab Navigation */}
        <div className="profile-tabs">
          <button
            className={`tab-button ${activeTab === 'profile' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            <FaUser className="tab-icon" />
            Profile
          </button>
          <button
            className={`tab-button ${activeTab === 'schedules' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('schedules')}
          >
            <FaBook className="tab-icon" />
            Learning Schedules
          </button>
          <button
            className={`tab-button ${activeTab === 'settings' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            <FaCog className="tab-icon" />
            Settings
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'profile' && (
            <ProfileTab 
              user={user} 
              isEditing={isEditing}
              setIsEditing={setIsEditing}
              onSave={handleSaveProfile}
            />
          )}

          {activeTab === 'schedules' && (
            <SchedulesTab 
              schedules={savedSchedules}
              onDeleteSchedule={deleteSchedule}
            />
          )}

          {activeTab === 'settings' && (
            <SettingsTab user={user} />
          )}
        </div>
      </div>
    </motion.div>
  );
};

// Profile Tab Component
const ProfileTab = ({ user, isEditing, setIsEditing, onSave }) => {
  const [editedUser, setEditedUser] = useState(user);
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onSave(editedUser);
    } catch (err) {
      // Error is handled in parent component
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setEditedUser(user);
    setIsEditing(false);
  };

  useEffect(() => {
    setEditedUser(user);
  }, [user]);

  return (
    <div className="profile-tab-content">
      <GlassCard className="profile-card">
        <div className="profile-header-section">
          <div className="avatar-section">
            <img 
              src={user.avatar || '/default-avatar.png'} 
              alt={user.name} 
              className="profile-avatar" 
            />
            {!isEditing && (
              <button 
                className="edit-profile-btn"
                onClick={() => setIsEditing(true)}
                disabled={isSaving}
              >
                Edit Profile
              </button>
            )}
          </div>

          <div className="profile-stats">
            <div className="stat-item">
              <span className="stat-number">{user.stats?.schedulesCreated || 0}</span>
              <span className="stat-label">Schedules</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{user.stats?.totalStudyHours || 0}</span>
              <span className="stat-label">Hours</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{user.stats?.completedTopics || 0}</span>
              <span className="stat-label">Topics</span>
            </div>
          </div>
        </div>

        <div className="profile-details">
          {isEditing ? (
            <div className="edit-form">
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  value={editedUser.name || ''}
                  onChange={(e) => setEditedUser({...editedUser, name: e.target.value})}
                  className="form-input"
                  disabled={isSaving}
                />
              </div>
              <div className="form-group">
                <label>Bio</label>
                <textarea
                  value={editedUser.bio || ''}
                  onChange={(e) => setEditedUser({...editedUser, bio: e.target.value})}
                  className="form-textarea"
                  rows="3"
                  disabled={isSaving}
                  placeholder="Tell us about yourself and your learning goals..."
                />
              </div>
              <div className="form-group">
                <label>Learning Goals (comma separated)</label>
                <input
                  type="text"
                  value={editedUser.learningGoals ? editedUser.learningGoals.join(', ') : ''}
                  onChange={(e) => setEditedUser({
                    ...editedUser, 
                    learningGoals: e.target.value.split(',').map(goal => goal.trim()).filter(goal => goal)
                  })}
                  className="form-input"
                  disabled={isSaving}
                  placeholder="e.g., Master React, Learn Python, Build Projects"
                />
              </div>
              <div className="form-actions">
                <button 
                  onClick={handleSave} 
                  className="save-btn"
                  disabled={isSaving}
                >
                  <FaCheckCircle className="btn-icon" />
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </button>
                <button 
                  onClick={handleCancel} 
                  className="cancel-btn"
                  disabled={isSaving}
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <h2 className="profile-name">{user.name || 'User'}</h2>
              <p className="profile-email">{user.email}</p>
              <p className="profile-bio">{user.bio || 'No bio provided yet.'}</p>
              <div className="join-date">
                Member since {user.joinDate ? new Date(user.joinDate).toLocaleDateString() : 'Recently'}
              </div>
              
              <div className="learning-goals">
                <h3>Learning Goals</h3>
                <div className="goals-list">
                  {user.learningGoals && user.learningGoals.length > 0 ? (
                    user.learningGoals.map((goal, index) => (
                      <span key={index} className="goal-tag">{goal}</span>
                    ))
                  ) : (
                    <p className="no-goals">No learning goals set yet.</p>
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      </GlassCard>
    </div>
  );
};

// Schedules Tab Component
const SchedulesTab = ({ schedules, onDeleteSchedule }) => {
  const [deletingId, setDeletingId] = useState(null);

  const handleDelete = async (scheduleId) => {
    setDeletingId(scheduleId);
    try {
      await onDeleteSchedule(scheduleId);
    } catch (err) {
      // Error handled in parent
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="schedules-tab-content">
      <GlassCard className="schedules-header">
        <h2>Your Learning Schedules</h2>
        <p className="schedules-count">
          {schedules.length} schedule{schedules.length !== 1 ? 's' : ''} created
        </p>
      </GlassCard>

      <div className="schedules-grid">
        {schedules.map((schedule) => (
          <motion.div
            key={schedule.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="schedule-card-wrapper"
          >
            <GlassCard className="schedule-card">
              <div className="schedule-header">
                <h3 className="schedule-title">{schedule.title}</h3>
                <button
                  onClick={() => handleDelete(schedule.id)}
                  className="delete-schedule-btn"
                  title="Delete schedule"
                  disabled={deletingId === schedule.id}
                >
                  {deletingId === schedule.id ? (
                    <div className="loading-spinner-small"></div>
                  ) : (
                    <FaTrash className="delete-icon" />
                  )}
                </button>
              </div>
              
              <div className="schedule-meta">
                <span className="meta-item">
                  <FaCalendar className="meta-icon" />
                  {formatDate(schedule.createdDate)}
                </span>
                <span className="meta-item">
                  <FaClock className="meta-icon" />
                  {schedule.duration}
                </span>
                <span className="meta-item">
                  <FaClock className="meta-icon" />
                  {schedule.totalHours} hours
                </span>
                <span className="meta-item">
                  <FaBookOpen className="meta-icon" />
                  {schedule.resourceCount || schedule.resources?.length || 0} resources
                </span>
              </div>

              <div className="schedule-topics">
                <h4>Topics Covered:</h4>
                <div className="topics-list">
                  {schedule.topics && schedule.topics.slice(0, 4).map((topic, index) => (
                    <span key={index} className="topic-tag">{topic}</span>
                  ))}
                  {schedule.topics && schedule.topics.length > 4 && (
                    <span className="topic-tag">+{schedule.topics.length - 4} more</span>
                  )}
                </div>
              </div>

              <div className="schedule-actions">
                <button className="action-btn view-btn">
                  <FaEye className="btn-icon" />
                  View Schedule
                </button>
                <button className="action-btn continue-btn">
                  <FaPlay className="btn-icon" />
                  Continue Learning
                </button>
              </div>

              {schedule.progress && (
                <div className="schedule-progress">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${schedule.progress}%` }}
                    ></div>
                  </div>
                  <span className="progress-text">{schedule.progress}% Complete</span>
                </div>
              )}
            </GlassCard>
          </motion.div>
        ))}
      </div>

      {schedules.length === 0 && (
        <GlassCard className="empty-state">
          <div className="empty-content">
            <h3>No schedules yet</h3>
            <p>Create your first learning schedule to get started!</p>
            <button 
              className="create-first-btn"
              onClick={() => window.location.href = '/schedule'}
            >
              <FaBook className="btn-icon" />
              Create Schedule
            </button>
          </div>
        </GlassCard>
      )}
    </div>
  );
};

// Settings Tab Component
const SettingsTab = ({ user }) => {
  const [settings, setSettings] = useState({
    emailNotifications: true,
    weeklyProgress: true,
    newFeatures: false,
    language: 'en',
    theme: 'auto'
  });
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/users/preferences', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        if (response.ok) {
          const savedSettings = await response.json();
          setSettings(savedSettings);
        }
      } catch (err) {
        console.error('Error loading settings:', err);
      }
    };
    loadSettings();
  }, []);

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const saveSettings = async () => {
    setIsSaving(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/users/preferences', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });

      if (!response.ok) {
        throw new Error('Failed to save settings');
      }

      alert('Settings saved successfully!');
    } catch (err) {
      alert('Failed to save settings');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="settings-tab-content">
      <GlassCard className="settings-card">
        <h2>Account Settings</h2>
        
        <div className="settings-section">
          <h3>
            <FaBell className="section-icon" />
            Notifications
          </h3>
          <div className="setting-item">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={settings.emailNotifications}
                onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
              />
              <FaEnvelope className="setting-icon" />
              <span>Email notifications</span>
            </label>
          </div>
          <div className="setting-item">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={settings.weeklyProgress}
                onChange={(e) => handleSettingChange('weeklyProgress', e.target.checked)}
              />
              <FaChartLine className="setting-icon" />
              <span>Weekly progress reports</span>
            </label>
          </div>
          <div className="setting-item">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={settings.newFeatures}
                onChange={(e) => handleSettingChange('newFeatures', e.target.checked)}
              />
              <FaBell className="setting-icon" />
              <span>New feature announcements</span>
            </label>
          </div>
        </div>

        <div className="settings-section">
          <h3>
            <FaCog className="section-icon" />
            Preferences
          </h3>
          <div className="setting-item">
            <label className="setting-label">
              <FaGlobe className="setting-icon" />
              Language
            </label>
            <select 
              value={settings.language}
              onChange={(e) => handleSettingChange('language', e.target.value)}
              className="setting-select"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
            </select>
          </div>
          <div className="setting-item">
            <label className="setting-label">
              <FaPalette className="setting-icon" />
              Theme
            </label>
            <select 
              value={settings.theme}
              onChange={(e) => handleSettingChange('theme', e.target.value)}
              className="setting-select"
            >
              <option value="auto">Auto</option>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>
        </div>

        <div className="settings-actions">
          <button 
            className="save-settings-btn"
            onClick={saveSettings}
            disabled={isSaving}
          >
            <FaCheckCircle className="btn-icon" />
            {isSaving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </GlassCard>
    </div>
  );
};

export default Profile;