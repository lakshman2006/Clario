import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Navbar from './components/Navbar';
import AnimatedBackground from './components/AnimatedBackground';
import MainPage from './pages/MainPage';
import BookRecommendations from './pages/BookRecommendations';
import Login from './pages/Login';
import AboutUs from './pages/AboutUs';
import ScheduleMaker from './pages/ScheduleMaker';

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<MainPage />} />
        <Route path="/books" element={<BookRecommendations />} />
        <Route path="/login" element={<Login />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/schedule" element={<ScheduleMaker />} />
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen relative">
        <AnimatedBackground />
        <Navbar />
        <AnimatedRoutes />
      </div>
    </Router>
  );
}

export default App;