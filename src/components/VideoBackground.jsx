import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';

const VideoBackground = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const videoRef = useRef(null);

  const handleVideoLoad = () => {
    setIsLoaded(true);
    // Ensure video plays and loops
    if (videoRef.current) {
      videoRef.current.play();
    }
  };

  return (
    <div className="video-background-container">
      {/* Video Element */}
      <motion.video
        ref={videoRef}
        className="background-video"
        autoPlay
        muted
        loop
        playsInline
        preload="auto"
        onLoadedData={handleVideoLoad}
        initial={{ opacity: 0 }}
        animate={{ opacity: isLoaded ? 1 : 0 }}
        transition={{ duration: 1.5 }}
      >
        {<source src="/your-video-filename.mp4" type="video/mp4" />}
        <source src="/background-video.mp4" type="video/mp4" />
        <source src="/background-video.webm" type="video/webm" />
        Your browser does not support the video tag.
      </motion.video>

      {/* Loading overlay */}
      {!isLoaded && (
        <motion.div
          className="video-loading-overlay"
          initial={{ opacity: 1 }}
          animate={{ opacity: isLoaded ? 0 : 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="loading-spinner"></div>
        </motion.div>
      )}

      {/* Gradient overlay for better text readability */}
      <div className="video-overlay"></div>
    </div>
  );
};

export default VideoBackground;