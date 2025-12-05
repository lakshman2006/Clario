import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { FaGoogle } from 'react-icons/fa';
import { setToken } from '../utils/auth';

const Login = () => {
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  const handleGoogleLogin = () => {
    // Redirect to backend OAuth endpoint
    // This will either go to Google OAuth or test login depending on configuration
    window.location.href = 'http://localhost:8000/api/v1/auth/google/login';
  };

  const handleTestLogin = async () => {
    try {
      setStatus('Testing login...');
      const response = await fetch('http://localhost:8000/api/v1/auth/test-login');
      const result = await response.json();
      
      if (result.status === 'success' && result.data?.access_token) {
        setToken(result.data.access_token);
        setStatus('Test login successful! Redirecting...');
        setTimeout(() => navigate('/profile'), 1500);
      } else {
        throw new Error('Test login failed');
      }
    } catch (error) {
      console.error('Test login error:', error);
      setStatus(`Test login failed: ${error.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
    <motion.div
        initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 w-full max-w-md border border-white/20"
        >
        <div className="text-center mb-8">
          <motion.h1
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-3xl font-bold text-white mb-2"
          >
            Welcome to Clario
          </motion.h1>
          <p className="text-blue-200">Sign in to continue your learning journey</p>
          </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleGoogleLogin}
          className="w-full bg-white text-gray-800 py-3 px-6 rounded-lg font-semibold flex items-center justify-center gap-3 hover:bg-gray-100 transition-colors mb-4"
        >
          <FaGoogle className="text-red-500" />
          Continue with Google
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleTestLogin}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          Test Login (Development)
        </motion.button>

        {status && (
          <div className="mt-4 text-center">
            <p className="text-blue-200 text-sm">{status}</p>
              </div>
            )}

        <div className="mt-6 text-center">
          <p className="text-blue-200 text-sm">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
                </div>

        <div className="mt-8 text-center">
          <p className="text-blue-300 text-xs">
            Clario uses Google OAuth for secure authentication
            </p>
          </div>
      </motion.div>
      </div>
  );
};

export default Login;