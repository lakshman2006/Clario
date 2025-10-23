import React, { useState } from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/GlassCard';
import BookCarousel from '../components/BookCarousel';
import { sampleBooks } from '../data/sampleBooks';

const BookRecommendations = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFormat, setSelectedFormat] = useState('all');
  const [books, setBooks] = useState(sampleBooks); // Show all books initially

  const formats = [
    { value: 'all', label: 'All Formats' },
    { value: 'PDF', label: 'PDF' },
    { value: 'eBook', label: 'eBook' },
    { value: 'Physical', label: 'Physical' }
  ];

  const handleSearch = () => {
    if (searchQuery.trim() === '') {
      setBooks(sampleBooks);
      return;
    }

    const filteredBooks = sampleBooks.filter(book => 
      book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.format.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setBooks(filteredBooks);
  };

  const filteredBooks = selectedFormat === 'all' 
    ? books 
    : books.filter(book => book.format === selectedFormat);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="min-h-screen py-12"
    >
      <div className="container">
        <GlassCard className="p-8 max-w-4xl mx-auto mb-12">
          <h1 className="text-4xl font-bold text-center mb-8">Book Recommendations</h1>

          {/* Search Section */}
          <div className="search-section">
            <div className="search-container">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Search for subjects, topics, or authors..."
                className="search-input"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSearch}
                className="search-btn"
              >
                Search
              </motion.button>
            </div>
          </div>

          {/* Format Toggle Section */}
          <div className="toggle-section">
            <h3 className="toggle-title">Filter by Format:</h3>
            <div className="toggle-container">
              {formats.map((format) => (
                <motion.button
                  key={format.value}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedFormat(format.value)}
                  className={`format-toggle ${selectedFormat === format.value ? 'format-toggle-active' : ''}`}
                >
                  {format.label}
                </motion.button>
              ))}
            </div>
          </div>

          {/* Results Count */}
          <div className="results-info">
            <p className="results-text">
              Showing {filteredBooks.length} book{filteredBooks.length !== 1 ? 's' : ''}
              {selectedFormat !== 'all' && ` in ${selectedFormat} format`}
              {searchQuery && ` for "${searchQuery}"`}
            </p>
          </div>
        </GlassCard>

        {/* Books Display */}
        {filteredBooks.length > 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <h2 className="section-title">Recommended Books</h2>
            <BookCarousel books={filteredBooks} />
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="no-results"
          >
            <GlassCard className="p-8 text-center">
              <h3 className="no-results-title">No books found</h3>
              <p className="no-results-text">
                Try adjusting your search or filter criteria
              </p>
            </GlassCard>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default BookRecommendations;