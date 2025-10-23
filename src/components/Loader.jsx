import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Loader = ({ onLoadingComplete }) => {
  const [progress, setProgress] = useState(0);
  const [currentTip, setCurrentTip] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const loadingTips = [
    "Craft your personalized learning path...",
    "Discover the best resources for you...",
    "Analyze your available time...",
    "Optimize your study schedule...",
  ];

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setIsComplete(true);
          setTimeout(() => {
            onLoadingComplete();
          }, 1000);
          return 100;
        }
        return prev + Math.random() * 15;
      });
    }, 300);

    const tipInterval = setInterval(() => {
      setCurrentTip(prev => (prev + 1) % loadingTips.length);
    }, 2000);

    return () => {
      clearInterval(progressInterval);
      clearInterval(tipInterval);
    };
  }, [onLoadingComplete, loadingTips.length]);

  return (
    <AnimatePresence>
      {!isComplete && (
        <motion.div
          className="loader-container"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ 
            opacity: 0,
            transition: { duration: 0.8, ease: "easeInOut" }
          }}
        >
          {/* Main Content */}
          <div className="loader-content">
            {/* Logo Container */}
            <motion.div
              className="logo-container"
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ 
                type: "spring", 
                stiffness: 200, 
                damping: 15,
                duration: 1 
              }}
            >
              <motion.div
                className="logo-orb"
                animate={{
                  scale: [1, 1.1, 1],
                  boxShadow: [
                    '0 0 20px rgba(121, 78, 131, 0.5)',
                    '0 0 40px rgba(121, 78, 131, 0.8)',
                    '0 0 20px rgba(121, 78, 131, 0.5)'
                  ],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                {/* Your Website Logo */}
                <img 
                  src="/logo.png" 
                  alt="CLARIO" 
                  className="loader-logo"
                />
              </motion.div>
            </motion.div>

            {/* Title */}
            <motion.h1
              className="loader-title"
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3, type: "spring", stiffness: 100 }}
            >
              CLARIO
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              className="loader-subtitle"
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5, type: "spring", stiffness: 100 }}
            >
              Learning Path Recommender
            </motion.p>

            {/* Progress Bar */}
            <motion.div
              className="progress-container"
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ delay: 0.7, duration: 0.5 }}
            >
              <motion.div
                className="progress-bar"
                initial={{ scaleX: 0 }}
                animate={{ scaleX: progress / 100 }}
                transition={{ type: "spring", stiffness: 100, damping: 15 }}
              />
              <div className="progress-text">
                {Math.round(progress)}%
              </div>
            </motion.div>

            {/* Loading Tips */}
            <motion.div
              className="tips-container"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9 }}
            >
              <AnimatePresence mode="wait">
                <motion.p
                  key={currentTip}
                  className="loading-tip"
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -20, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  {loadingTips[currentTip]}
                </motion.p>
              </AnimatePresence>
            </motion.div>

            {/* Animated Dots */}
            <motion.div className="dots-container">
              {[0, 1, 2].map((index) => (
                <motion.div
                  key={index}
                  className="dot"
                  animate={{
                    y: [0, -10, 0],
                    opacity: [0.3, 1, 0.3],
                  }}
                  transition={{
                    duration: 1,
                    repeat: Infinity,
                    delay: index * 0.2,
                    ease: "easeInOut"
                  }}
                />
              ))}
            </motion.div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Loader;