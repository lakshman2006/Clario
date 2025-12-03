import pandas as pd
import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Handles loading and preprocessing of learning resource data.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.resources_file = os.path.join(data_dir, "resources.csv")
    
    def load_resources(self) -> pd.DataFrame:
        """
        Load resources data from CSV file.
        
        Returns:
            DataFrame with resource data
        """
        try:
            if os.path.exists(self.resources_file):
                df = pd.read_csv(self.resources_file)
                logger.info(f"Loaded {len(df)} resources from {self.resources_file}")
                return df
            else:
                # Create sample data if file doesn't exist
                logger.warning(f"Resources file not found at {self.resources_file}, creating sample data")
                return self._create_sample_data()
                
        except Exception as e:
            logger.error(f"Error loading resources: {e}")
            return self._create_sample_data()
    
    def _create_sample_data(self) -> pd.DataFrame:
        """Create sample resource data for testing."""
        sample_data = [
            {
                "id": 1,
                "title": "Introduction to Machine Learning",
                "description": "Learn the fundamentals of machine learning algorithms and applications",
                "type": "video",
                "url": "https://example.com/ml-intro",
                "difficulty": "beginner",
                "duration": 60,
                "tags": "machine learning, AI, algorithms"
            },
            {
                "id": 2,
                "title": "Deep Learning with Python",
                "description": "Comprehensive guide to deep learning using Python and TensorFlow",
                "type": "book",
                "url": "https://example.com/deep-learning-book",
                "difficulty": "intermediate",
                "duration": 480,
                "tags": "deep learning, neural networks, python"
            },
            {
                "id": 3,
                "title": "Data Science Fundamentals",
                "description": "Essential concepts in data science and statistical analysis",
                "type": "course",
                "url": "https://example.com/data-science-course",
                "difficulty": "beginner",
                "duration": 120,
                "tags": "data science, statistics, analysis"
            },
            {
                "id": 4,
                "title": "Advanced Python Programming",
                "description": "Master advanced Python concepts and best practices",
                "type": "video",
                "url": "https://example.com/advanced-python",
                "difficulty": "advanced",
                "duration": 90,
                "tags": "python, programming, advanced"
            },
            {
                "id": 5,
                "title": "Web Development with React",
                "description": "Build modern web applications using React and JavaScript",
                "type": "course",
                "url": "https://example.com/react-course",
                "difficulty": "intermediate",
                "duration": 180,
                "tags": "react, javascript, web development"
            },
            {
                "id": 6,
                "title": "Database Design Principles",
                "description": "Learn how to design efficient and scalable databases",
                "type": "article",
                "url": "https://example.com/database-design",
                "difficulty": "intermediate",
                "duration": 30,
                "tags": "database, design, SQL"
            },
            {
                "id": 7,
                "title": "DevOps Best Practices",
                "description": "Essential DevOps practices for modern software development",
                "type": "video",
                "url": "https://example.com/devops-practices",
                "difficulty": "intermediate",
                "duration": 75,
                "tags": "devops, deployment, automation"
            },
            {
                "id": 8,
                "title": "Cybersecurity Fundamentals",
                "description": "Introduction to cybersecurity concepts and practices",
                "type": "course",
                "url": "https://example.com/cybersecurity-intro",
                "difficulty": "beginner",
                "duration": 150,
                "tags": "cybersecurity, security, networking"
            }
        ]
        
        df = pd.DataFrame(sample_data)
        
        # Save sample data to file
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            df.to_csv(self.resources_file, index=False)
            logger.info(f"Sample data saved to {self.resources_file}")
        except Exception as e:
            logger.warning(f"Could not save sample data: {e}")
        
        return df
    
    def get_resource_texts(self, df: pd.DataFrame) -> List[str]:
        """
        Extract text content from resources for ML processing.
        
        Args:
            df: Resources DataFrame
            
        Returns:
            List of combined text strings
        """
        try:
            texts = []
            for _, row in df.iterrows():
                # Combine title, description, and tags
                text_parts = [
                    str(row.get('title', '')),
                    str(row.get('description', '')),
                    str(row.get('tags', ''))
                ]
                combined_text = ' '.join(filter(None, text_parts))
                texts.append(combined_text)
            
            return texts
            
        except Exception as e:
            logger.error(f"Error extracting resource texts: {e}")
            return []
    
    def get_all_resource_types(self, df: pd.DataFrame) -> List[str]:
        """
        Get all unique resource types from the DataFrame.
        
        Args:
            df: Resources DataFrame
            
        Returns:
            List of unique resource types
        """
        try:
            types = df['type'].unique().tolist()
            return [str(t) for t in types if pd.notna(t)]
        except Exception as e:
            logger.error(f"Error getting resource types: {e}")
            return []