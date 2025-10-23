import React from 'react';
import { motion } from 'framer-motion';

const ImageBackground = () => {
  return (
    <div className="image-background-container">
      <motion.div
        className="background-image"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.5 }}
        style={{
          backgroundImage: `url('/background-image.jpg')` // Change this path to your image
        }}
      />
      
      {/* Optional overlay for better text readability */}
      <div className="image-overlay"></div>
    </div>
  );
};

export default ImageBackground;