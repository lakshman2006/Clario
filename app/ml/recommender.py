import pandas as pd
import os
from typing import List, Dict, Any, Tuple
from .utils.similarity import SimilarityCalculator
from .utils.loader import DataLoader
from .preprocess import preprocess_for_similarity

class LearningResourceRecommender:
    """
    Main recommendation engine for learning resources using TF-IDF and cosine similarity.
    """
    
    def __init__(self, data_dir: str = "app/ml/data", model_dir: str = "app/ml/model"):
        self.data_dir = data_dir
        self.model_dir = model_dir
        self.data_loader = DataLoader(data_dir)
        self.similarity_calc = SimilarityCalculator()
        self.resources_df = None
        self.resource_texts = None
        self.is_trained = False
        
        # Model file paths
        self.vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
    
    def load_data(self):
        """Load and prepare data for training."""
        try:
            # Load resources data
            self.resources_df = self.data_loader.load_resources()
            
            # Extract text for ML processing
            self.resource_texts = self.data_loader.get_resource_texts(self.resources_df)
            
            print(f"Loaded {len(self.resources_df)} resources")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def train_model(self):
        """Train the TF-IDF vectorizer on the resource texts."""
        if not self.resource_texts:
            raise ValueError("No data loaded. Call load_data() first.")
        
        if not self.resource_texts:
            raise ValueError("No resource texts available for training")
        
        # Preprocess texts
        processed_texts = [preprocess_for_similarity(text) for text in self.resource_texts]
        
        # Filter out empty texts
        processed_texts = [text for text in processed_texts if text.strip()]
        
        if not processed_texts:
            raise ValueError("No valid texts after preprocessing")
        
        # Fit the vectorizer
        self.similarity_calc.fit_vectorizer(processed_texts)
        self.is_trained = True
        
        # Save the model
        self.save_model()
        
        print("Model trained successfully")
    
    def save_model(self):
        """Save the trained model to disk."""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        os.makedirs(self.model_dir, exist_ok=True)
        self.similarity_calc.save_model(self.vectorizer_path)
        print(f"Model saved to {self.vectorizer_path}")
    
    def load_model(self):
        """Load a pre-trained model from disk."""
        try:
            self.similarity_calc.load_model(self.vectorizer_path)
            self.is_trained = True
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def initialize(self):
        """Initialize the recommender (load data and model)."""
        # Try to load existing model first
        if self.load_model():
            # If model loaded successfully, also load data
            self.load_data()
            return True
        else:
            # If no model exists, load data and train
            if self.load_data():
                self.train_model()
                return True
            else:
                return False
    
    def get_recommendations(self, topic: str, top_k: int = 5, filter_type: str = None) -> List[Dict[str, Any]]:
        """
        Get learning resource recommendations based on topic.
        
        Args:
            topic: User's topic of interest
            top_k: Number of recommendations to return
            filter_type: Optional resource type filter (video, article, course)
            
        Returns:
            List of recommendation dictionaries
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting recommendations")
        
        if not self.resources_df is not None:
            raise ValueError("Resources data not loaded")
        
        # Preprocess the query
        processed_topic = preprocess_for_similarity(topic)
        
        if not processed_topic.strip():
            raise ValueError("Topic query is empty after preprocessing")
        
        # Get similarity scores
        similarities = self.similarity_calc.calculate_similarity(processed_topic, self.resource_texts)
        
        # Get top-k indices
        top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:top_k]
        
        # Prepare recommendations
        recommendations = []
        
        for idx in top_indices:
            if idx < len(self.resources_df):
                resource = self.resources_df.iloc[idx]
                
                # Apply type filter if specified
                if filter_type and resource.get('type', '').lower() != filter_type.lower():
                    continue
                
                recommendation = {
                    'title': resource.get('title', ''),
                    'type': resource.get('type', ''),
                    'url': resource.get('url', ''),
                    'confidence': float(similarities[idx])
                }
                
                recommendations.append(recommendation)
        
        return recommendations
    
    def get_recommendations_by_type(self, topic: str, top_k: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recommendations categorized by resource type.
        
        Args:
            topic: User's topic of interest
            top_k: Number of recommendations per type
            
        Returns:
            Dictionary with type as key and recommendations as value
        """
        if not self.resources_df is not None:
            raise ValueError("Resources data not loaded")
        
        # Get all resource types
        resource_types = self.data_loader.get_all_resource_types(self.resources_df)
        
        recommendations_by_type = {}
        
        for resource_type in resource_types:
            type_recommendations = self.get_recommendations(
                topic=topic,
                top_k=top_k,
                filter_type=resource_type
            )
            
            if type_recommendations:
                recommendations_by_type[resource_type] = type_recommendations
        
        return recommendations_by_type
    
    def get_all_resource_types(self) -> List[str]:
        """Get list of all available resource types."""
        if self.resources_df is None:
            return []
        
        return self.data_loader.get_all_resource_types(self.resources_df)
