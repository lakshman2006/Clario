import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.ml.recommender import LearningResourceRecommender
from app.ml.preprocess import clean_text, tokenize_text
from app.ml.utils.similarity import SimilarityCalculator

class TestMLRecommender:
    """Test cases for the ML recommendation system."""
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        # Test basic cleaning
        assert clean_text("Hello World!") == "hello world"
        assert clean_text("Test123") == "test"
        assert clean_text("") == ""
        assert clean_text("   ") == ""
        
        # Test with special characters
        assert clean_text("Hello, World!") == "hello world"
        assert clean_text("Test-123") == "test"
    
    def test_tokenize_text(self):
        """Test text tokenization."""
        tokens = tokenize_text("Hello world")
        assert tokens == ["hello", "world"]
        
        tokens = tokenize_text("")
        assert tokens == []
        
        tokens = tokenize_text("   ")
        assert tokens == []
    
    def test_similarity_calculator(self):
        """Test similarity calculation functionality."""
        calc = SimilarityCalculator()
        
        documents = [
            "python programming tutorial",
            "machine learning basics",
            "web development guide"
        ]
        
        # Fit the vectorizer
        calc.fit_vectorizer(documents)
        
        # Test similarity calculation
        similarities = calc.calculate_similarity("python", documents)
        assert len(similarities) == 3
        assert all(0 <= score <= 1 for score in similarities)
        
        # Test top similar
        top_similar = calc.get_top_similar("python", documents, top_k=2)
        assert len(top_similar) == 2
        assert all(isinstance(item, tuple) and len(item) == 2 for item in top_similar)
    
    def test_recommender_initialization(self):
        """Test recommender initialization."""
        recommender = LearningResourceRecommender()
        
        # Test data loading
        success = recommender.load_data()
        assert success == True
        
        # Test that resources are loaded
        assert recommender.resources_df is not None
        assert len(recommender.resources_df) > 0
        
        # Test that resource texts are extracted
        assert recommender.resource_texts is not None
        assert len(recommender.resource_texts) > 0
    
    def test_recommender_training(self):
        """Test recommender training."""
        recommender = LearningResourceRecommender()
        
        # Load data
        recommender.load_data()
        
        # Train model
        recommender.train_model()
        
        # Check that model is trained
        assert recommender.is_trained == True
    
    def test_get_recommendations(self):
        """Test getting recommendations."""
        recommender = LearningResourceRecommender()
        
        # Initialize (load data and train)
        success = recommender.initialize()
        assert success == True
        
        # Get recommendations
        recommendations = recommender.get_recommendations("python", top_k=3)
        
        # Check recommendations format
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3
        
        if recommendations:
            rec = recommendations[0]
            assert "title" in rec
            assert "type" in rec
            assert "url" in rec
            assert "confidence" in rec
            assert isinstance(rec["confidence"], float)
    
    def test_get_recommendations_by_type(self):
        """Test getting recommendations by type."""
        recommender = LearningResourceRecommender()
        
        # Initialize
        success = recommender.initialize()
        assert success == True
        
        # Get recommendations by type
        recommendations_by_type = recommender.get_recommendations_by_type("python", top_k=2)
        
        # Check format
        assert isinstance(recommendations_by_type, dict)
        
        # Check that each type has recommendations
        for resource_type, recommendations in recommendations_by_type.items():
            assert isinstance(recommendations, list)
            assert len(recommendations) <= 2
            
            if recommendations:
                rec = recommendations[0]
                assert rec["type"] == resource_type

if __name__ == "__main__":
    pytest.main([__file__])
