import React from 'react';
import { motion } from 'framer-motion';

const AnimatedBackground = () => {
  return (
    <div className="abstract-background">
      {/* Main gradient with reduced motion */}
      <motion.div 
        className="main-gradient"
        animate={{
          background: [
            'radial-gradient(circle at 20% 80%, #d9c2e5 0%, #e5d0ff 30%, transparent 50%), radial-gradient(circle at 80% 20%, #f7d8e8 0%, #e4c4e7 30%, transparent 50%)',
            'radial-gradient(circle at 80% 80%, #e5d0ff 0%, #d9c2e5 30%, transparent 50%), radial-gradient(circle at 20% 20%, #e4c4e7 0%, #f7d8e8 30%, transparent 50%)',
          ],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          repeatType: 'reverse',
          ease: "easeInOut"
        }}
      />
      
      {/* Reduced number of particles for performance */}
      <motion.div
        className="floating-particle particle-1"
        animate={{
          x: [0, 50, 0],
          y: [0, -40, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          repeatType: 'reverse',
          ease: "easeInOut"
        }}
      />
      
      <motion.div
        className="floating-particle particle-2"
        animate={{
          x: [0, -60, 0],
          y: [0, 50, 0],
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          repeatType: 'reverse',
          ease: "easeInOut"
        }}
      />

      {/* Subtle overlay */}
      <motion.div 
        className="gradient-overlay"
        animate={{
          opacity: [0.1, 0.2, 0.1],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          repeatType: 'reverse',
          ease: "easeInOut"
        }}
      />
    </div>
  );
};

export default AnimatedBackground;