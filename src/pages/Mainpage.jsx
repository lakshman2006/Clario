import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import GlassCard from '../components/GlassCard';

const MainPage = () => {
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen flex items-center justify-center"
    >
      <GlassCard className="p-12 text-center max-w-2xl">
        <motion.h1
          className="text-6xl font-bold mb-6"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 100, damping: 15, duration: 0.8 }}
        >
          CLARIO
        </motion.h1>
        <motion.p
          className="text-xl mb-8 opacity-80"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 100, damping: 15, duration: 0.8, delay: 0.1 }}
        >
          Your Personalized Learning Path Recommender 
        </motion.p>
        <motion.button
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 100, damping: 15, duration: 0.8, delay: 0.2 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => navigate('/schedule')}
          className="btn-primary text-lg px-8 py-4"
        >
          Make Your Own Schedule
        </motion.button>
      </GlassCard>
    </motion.div>
  );
};

export default MainPage;