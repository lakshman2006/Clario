"""
Book Recommendation System

This module provides intelligent book recommendations based on topic similarity.
Completely separate from the schedule maker functionality.
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from .utils.similarity import SimilarityCalculator
from .preprocess import preprocess_for_similarity
import logging

logger = logging.getLogger(__name__)

class BookRecommender:
    """
    Book recommendation engine using TF-IDF and cosine similarity.
    Focuses specifically on book recommendations based on topics.
    """
    
    def __init__(self, data_dir: str = "app/ml/data", model_dir: str = "app/ml/model"):
        self.data_dir = data_dir
        self.model_dir = model_dir
        self.similarity_calc = SimilarityCalculator()
        self.books_df = None
        self.book_texts = None
        self.is_trained = False
        
        # Model file paths
        self.vectorizer_path = os.path.join(model_dir, "book_vectorizer.pkl")
    
    def load_books_data(self):
        """Load and prepare book data for training."""
        try:
            books_file = os.path.join(self.data_dir, "books.csv")
            self.books_df = pd.read_csv(books_file)
            
            # Create combined text for ML processing
            self.book_texts = []
            for _, book in self.books_df.iterrows():
                # Combine title, author, genre, topic, and description for better matching
                combined_text = f"{book['title']} {book['author']} {book['genre']} {book['topic']} {book['description']}"
                self.book_texts.append(combined_text)
            
            logger.info(f"Loaded {len(self.books_df)} books for recommendation")
            return True
            
        except Exception as e:
            logger.error(f"Error loading book data: {e}")
            return False
    
    def train_model(self):
        """Train the TF-IDF vectorizer on book texts."""
        if not self.book_texts:
            raise ValueError("No book data loaded. Call load_books_data() first.")
        
        # Preprocess texts
        processed_texts = [preprocess_for_similarity(text) for text in self.book_texts]
        
        # Filter out empty texts
        processed_texts = [text for text in processed_texts if text.strip()]
        
        if not processed_texts:
            raise ValueError("No valid texts after preprocessing")
        
        # Fit the vectorizer
        self.similarity_calc.fit_vectorizer(processed_texts)
        self.is_trained = True
        
        # Save the model
        self.save_model()
        
        logger.info("Book recommendation model trained successfully")
    
    def save_model(self):
        """Save the trained model to disk."""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        os.makedirs(self.model_dir, exist_ok=True)
        self.similarity_calc.save_model(self.vectorizer_path)
        logger.info(f"Book model saved to {self.vectorizer_path}")
    
    def load_model(self):
        """Load a pre-trained model from disk."""
        try:
            self.similarity_calc.load_model(self.vectorizer_path)
            # Recreate fitted texts vectors after loading model
            if self.book_texts:
                processed_texts = [preprocess_for_similarity(text) for text in self.book_texts]
                processed_texts = [text for text in processed_texts if text.strip()]
                if processed_texts:
                    self.similarity_calc.fitted_texts_vectors = self.similarity_calc.vectorizer.transform(processed_texts)
            self.is_trained = True
            logger.info("Book recommendation model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading book model: {e}")
            return False
    
    def initialize(self):
        """Initialize the book recommender (load data and model)."""
        # Load data first
        if not self.load_books_data():
            logger.error("Failed to load book data for recommendation.")
            return False
        
        # Try to load existing model
        if self.load_model():
            logger.info("Existing book recommendation model loaded.")
            return True
        
        logger.info("No existing book model found. Training new model...")
        
        try:
            self.train_model()
            logger.info("New book recommendation model trained and saved.")
            return True
        except Exception as e:
            logger.error(f"Error training new book model: {e}")
            return False

    def get_book_recommendations(
        self,
        topic: str,
        top_k: int = 5,
        genre: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        min_rating: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Get book recommendations based on a topic.

        Args:
            topic: The topic for which to get book recommendations
            top_k: Number of recommendations to return
            genre: Optional filter by genre
            difficulty_level: Optional filter by difficulty level
            min_rating: Minimum rating filter

        Returns:
            List of recommended books with similarity scores
        """
        if not self.is_trained:
            logger.warning("Book model not trained. Initializing now...")
            self.initialize()
            if not self.is_trained:
                logger.error("Book model failed to initialize. Cannot provide recommendations.")
                return []

        if self.books_df is None or self.books_df.empty:
            logger.warning("No books loaded. Cannot provide recommendations.")
            return []

        # Preprocess the topic
        processed_topic = preprocess_for_similarity(topic)
        if not processed_topic.strip():
            logger.warning("Processed topic is empty. Cannot provide recommendations.")
            return []

        # Get similarity scores
        similarities = self.similarity_calc.get_similarities(processed_topic)

        # Combine with book data
        recommendations_df = self.books_df.copy()
        recommendations_df['similarity_score'] = similarities

        # Apply filters
        if genre:
            recommendations_df = recommendations_df[
                recommendations_df['genre'].str.lower() == genre.lower()
            ]
        
        if difficulty_level:
            recommendations_df = recommendations_df[
                recommendations_df['difficulty_level'].str.lower() == difficulty_level.lower()
            ]
        
        if min_rating > 0:
            recommendations_df = recommendations_df[
                recommendations_df['rating'].astype(float) >= min_rating
            ]

        # Sort by similarity and get top_k
        recommendations_df = recommendations_df.sort_values(by='similarity_score', ascending=False)
        top_recommendations = recommendations_df.head(top_k)

        # Format output
        result = []
        for _, book in top_recommendations.iterrows():
            result.append({
                "id": int(book['id']),
                "title": book['title'],
                "author": book['author'],
                "genre": book['genre'],
                "topic": book['topic'],
                "description": book['description'],
                "rating": float(book['rating']),
                "price": book['price'],
                "isbn": book['isbn'],
                "amazon_url": book['amazon_url'],
                "goodreads_url": book['goodreads_url'],
                "publication_year": int(book['publication_year']),
                "pages": int(book['pages']),
                "language": book['language'],
                "difficulty_level": book['difficulty_level'],
                "similarity_score": round(book['similarity_score'], 3)
            })

        logger.info(f"Generated {len(result)} book recommendations for topic '{topic}'")
        return result

    def search_books(
        self,
        query: str,
        top_k: int = 10,
        genre: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search books by title, author, or description.

        Args:
            query: Search query
            top_k: Number of results to return
            genre: Optional genre filter

        Returns:
            List of matching books
        """
        if self.books_df is None:
            self.load_books_data()
        
        if self.books_df is None or self.books_df.empty:
            return []

        # Simple text search across title, author, and description
        search_df = self.books_df.copy()
        
        # Create search text
        search_df['search_text'] = (
            search_df['title'].str.lower() + ' ' +
            search_df['author'].str.lower() + ' ' +
            search_df['description'].str.lower()
        )
        
        # Filter by genre if specified
        if genre:
            search_df = search_df[search_df['genre'].str.lower() == genre.lower()]
        
        # Search for query in search_text
        query_lower = query.lower()
        mask = search_df['search_text'].str.contains(query_lower, na=False)
        results_df = search_df[mask].head(top_k)
        
        # Format results
        result = []
        for _, book in results_df.iterrows():
            result.append({
                "id": int(book['id']),
                "title": book['title'],
                "author": book['author'],
                "genre": book['genre'],
                "topic": book['topic'],
                "description": book['description'],
                "rating": float(book['rating']),
                "price": book['price'],
                "difficulty_level": book['difficulty_level']
            })
        
        return result
