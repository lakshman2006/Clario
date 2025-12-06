import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SimilarityCalculator:
    """
    Handles TF-IDF vectorization and cosine similarity calculations.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        self.is_fitted = False
    
    def fit_vectorizer(self, texts: List[str]):
        """Fit the TF-IDF vectorizer on texts."""
        try:
            self.vectorizer.fit(texts)
            # Store the fitted text vectors for later use
            self.fitted_texts_vectors = self.vectorizer.transform(texts)
            self.is_fitted = True
            logger.info("TF-IDF vectorizer fitted successfully")
        except Exception as e:
            logger.error(f"Error fitting vectorizer: {e}")
            raise
    
    def calculate_similarity(self, query: str, texts: List[str]) -> List[float]:
        """
        Calculate cosine similarity between query and texts.
        
        Args:
            query: Query text
            texts: List of texts to compare against
            
        Returns:
            List of similarity scores
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted before calculating similarity")
        
        try:
            # Transform query and texts
            query_vector = self.vectorizer.transform([query])
            text_vectors = self.vectorizer.transform(texts)
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, text_vectors).flatten()
            
            return similarities.tolist()
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            raise
    
    def get_similarities(self, query: str) -> List[float]:
        """
        Get similarity scores for a query against the fitted texts.
        This method assumes the vectorizer has been fitted and the texts are stored.
        
        Args:
            query: Query text
            
        Returns:
            List of similarity scores
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted before getting similarities")
        
        try:
            # Transform query
            query_vector = self.vectorizer.transform([query])
            
            # Get the fitted texts (we need to store them during fitting)
            if not hasattr(self, 'fitted_texts_vectors'):
                raise ValueError("No fitted texts available. Call fit_vectorizer with texts first.")
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, self.fitted_texts_vectors).flatten()
            
            return similarities.tolist()
            
        except Exception as e:
            logger.error(f"Error getting similarities: {e}")
            raise
    
    def save_model(self, filepath: str):
        """Save the fitted vectorizer to disk."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            logger.info(f"Model saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    def load_model(self, filepath: str):
        """Load a fitted vectorizer from disk."""
        try:
            with open(filepath, 'rb') as f:
                self.vectorizer = pickle.load(f)
            self.is_fitted = True
            # Note: fitted_texts_vectors are not saved/loaded, they need to be recreated
            logger.info(f"Model loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise