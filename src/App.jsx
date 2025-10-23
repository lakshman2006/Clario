import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import Navbar from './components/Navbar';
import ImageBackground from './components/ImageBackground';
import Loader from './components/Loader';
import Footer from './components/Footer';
import MainPage from './pages/MainPage';
import BookRecommendations from './pages/BookRecommendations';
import Login from './pages/Login';
import AboutUs from './pages/AboutUs';
import ScheduleMaker from './pages/ScheduleMaker';
import Profile from './pages/Profile'; 

const pageVariants = {
  initial: {
    opacity: 0,
    scale: 0.98,
    y: 10
  },
  in: {
    opacity: 1,
    scale: 1,
    y: 0
  },
  out: {
    opacity: 0,
    scale: 1.02,
    y: -10
  }
};

const pageTransition = {
  type: "tween",
  ease: "anticipate",
  duration: 0.4
};

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={
          <motion.div
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <MainPage />
          </motion.div>
        } />
        <Route path="/books" element={
          <motion.div
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <BookRecommendations />
          </motion.div>
        } />
        <Route path="/login" element={
          <motion.div
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <Login />
          </motion.div>
        } />
        <Route path="/about" element={
          <motion.div
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <AboutUs />
          </motion.div>
        } />
        <Route path="/schedule" element={
          <motion.div
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <ScheduleMaker />
          </motion.div>
        } />
        {/* ADD THE PROFILE ROUTE */}
        <Route path="/profile" element={
          <motion.div
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <Profile />
          </motion.div>
        } />
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  const [isLoading, setIsLoading] = useState(true);

  const handleLoadingComplete = () => {
    setIsLoading(false);
  };

  return (
    <Router>
      <div className="smooth-website">
        <AnimatePresence mode="wait">
          {isLoading ? (
            <Loader onLoadingComplete={handleLoadingComplete} />
          ) : (
            <motion.div
              key="main-app"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="app-container"
            >
              <ImageBackground />
              <Navbar />
              <main className="main-content">
                <AnimatedRoutes />
              </main>
              <Footer />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Router>
  );
}

export default App;