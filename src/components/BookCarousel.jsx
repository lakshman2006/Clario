
import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import GlassCard from './GlassCard';

const BookCarousel = ({ books }) => {
  const [position, setPosition] = useState(0);
  const [selectedBook, setSelectedBook] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const carouselRef = useRef(null);

  const maxPosition = Math.max(0, books.length - 3);

  const nextSlide = () => {
    setPosition(prev => Math.min(prev + 1, maxPosition));
  };

  const prevSlide = () => {
    setPosition(prev => Math.max(prev - 1, 0));
  };

  const dragEndHandler = (event, info) => {
    setIsDragging(false);
    const threshold = 50;
    if (Math.abs(info.offset.x) > threshold) {
      if (info.offset.x > 0) {
        prevSlide();
      } else {
        nextSlide();
      }
    }
  };

  const openBookDetails = (book) => {
    if (!isDragging) {
      setSelectedBook(book);
    }
  };

  const closeBookDetails = () => {
    setSelectedBook(null);
  };

  return (
    <div className="enhanced-carousel-container">
      {/* Navigation Arrows */}
      {position > 0 && (
        <motion.button
          className="carousel-arrow carousel-arrow-left"
          onClick={prevSlide}
          whileHover={{ scale: 1.1, x: -5 }}
          whileTap={{ scale: 0.9 }}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          ‹
        </motion.button>
      )}

      {position < maxPosition && (
        <motion.button
          className="carousel-arrow carousel-arrow-right"
          onClick={nextSlide}
          whileHover={{ scale: 1.1, x: 5 }}
          whileTap={{ scale: 0.9 }}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          ›
        </motion.button>
      )}

      {/* Carousel Track */}
      <motion.div
        ref={carouselRef}
        className="enhanced-carousel-track"
        drag="x"
        dragConstraints={{ left: -320 * maxPosition, right: 0 }}
        dragElastic={0.1}
        onDragStart={() => setIsDragging(true)}
        onDragEnd={dragEndHandler}
        animate={{ x: -position * 320 }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
      >
        {books.map((book, index) => (
          <motion.div
            key={book.id}
            className="book-card-wrapper"
            initial={{ opacity: 0, y: 50, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: index * 0.1, type: "spring", stiffness: 100 }}
            whileHover={{ 
              scale: 1.05,
              y: -10,
              transition: { type: "spring", stiffness: 400 }
            }}
          >
            <GlassCard className="enhanced-book-card">
              {/* Book Cover with Glow Effect */}
              <div className="book-cover-container">
                <motion.img
                  src={book.cover}
                  alt={book.title}
                  className="book-cover"
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: "spring", stiffness: 300 }}
                />
                <div className="book-cover-glow"></div>
                
                {/* Format Badge */}
                <div className={`format-badge format-${book.format.toLowerCase()}`}>
                  {book.format}
                </div>
              </div>

              {/* Book Info */}
              <div className="book-info">
                <h3 className="book-title">{book.title}</h3>
                <p className="book-author">by {book.author}</p>
                
                {/* Book Details */}
                <div className="book-details">
                  {book.genre && (
                    <span className="book-genre">{book.genre}</span>
                  )}
                  {book.difficulty_level && (
                    <span className={`book-difficulty difficulty-${book.difficulty_level.toLowerCase()}`}>
                      {book.difficulty_level}
                    </span>
                  )}
                  {book.publication_year && (
                    <span className="book-year">{book.publication_year}</span>
                  )}
                </div>
                
                {/* Rating Stars */}
                <div className="book-rating">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span
                      key={star}
                      className={`rating-star ${star <= (book.rating || 4) ? 'filled' : ''}`}
                    >
                      ★
                    </span>
                  ))}
                  <span className="rating-text">{(book.rating || 4).toFixed(1)}</span>
                </div>
                
                {/* Price and Links */}
                <div className="book-actions">
                  {book.price && (
                    <span className="book-price">{book.price}</span>
                  )}
                  {book.amazon_url && (
                    <a 
                      href={book.amazon_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="book-link amazon-link"
                    >
                      Amazon
                    </a>
                  )}
                  {book.goodreads_url && (
                    <a 
                      href={book.goodreads_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="book-link goodreads-link"
                    >
                      Goodreads
                    </a>
                  )}
                </div>
                
                {/* Similarity Score (for recommendations) */}
                {book.similarity_score && (
                  <div className="similarity-score">
                    Match: {(book.similarity_score * 100).toFixed(1)}%
                  </div>
                )}
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </motion.div>

      {/* Progress Dots */}
      {books.length > 3 && (
        <div className="carousel-dots">
          {Array.from({ length: maxPosition + 1 }).map((_, index) => (
            <button
              key={index}
              className={`carousel-dot ${index === position ? 'active' : ''}`}
              onClick={() => setPosition(index)}
            />
          ))}
        </div>
      )}

      </div>
  );
};

export default BookCarousel;