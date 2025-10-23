import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate, useLocation } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { name: 'Book Recommendations', path: '/books' },
    { name: 'About Us', path: '/about' },
    { name: 'Login', path: '/login' },
    { name: 'Profile', path: '/profile' },
  ];

  const navVariants = {
    hidden: { y: -100, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 30,
        duration: 0.6
      }
    }
  };

  const itemVariants = {
    hidden: { y: -20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 400,
        damping: 25
      }
    }
  };

  return (
    <motion.nav
      className="glass-card mx-4 mt-4 mb-8"
      variants={navVariants}
      initial="hidden"
      animate="visible"
    >
      <div className="container">
        <div className="navbar">
          <motion.button
            variants={itemVariants}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/')}
            className="nav-logo"
            transition={{ type: "spring", stiffness: 400, damping: 17 }}
          >
            <img src="/logo.png" alt="CLARIO" className="h-10 w-10" />
            <span className="text-2xl font-bold">CLARIO</span>
          </motion.button>

          <div className="nav-items">
            {navItems.map((item, index) => (
              <motion.button
                key={item.name}
                variants={itemVariants}
                custom={index}
                initial="hidden"
                animate="visible"
                transition={{ delay: index * 0.1 + 0.3 }}
                whileHover={{ 
                  scale: 1.05,
                  transition: { type: "spring", stiffness: 400, damping: 10 }
                }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate(item.path)}
                className={`nav-button ${location.pathname === item.path ? 'active' : ''}`}
              >
                {item.name}
              </motion.button>
            ))}
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;