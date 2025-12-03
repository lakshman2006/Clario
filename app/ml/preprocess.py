import re
import string
from typing import List
import logging

logger = logging.getLogger(__name__)

def preprocess_for_similarity(text: str) -> str:
    """
    Preprocess text for similarity calculation.
    
    Args:
        text: Raw text to preprocess
        
    Returns:
        Preprocessed text
    """
    if not text or not isinstance(text, str):
        return ""
    
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
        
    except Exception as e:
        logger.error(f"Error preprocessing text: {e}")
        return ""

def clean_text(text: str) -> str:
    """
    Basic text cleaning for display purposes.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text or not isinstance(text, str):
        return ""
    
    try:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
        
    except Exception as e:
        logger.error(f"Error cleaning text: {e}")
        return ""

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keywords
    """
    if not text or not isinstance(text, str):
        return []
    
    try:
        # Preprocess text
        processed_text = preprocess_for_similarity(text)
        
        # Split into words
        words = processed_text.split()
        
        # Remove common stop words (basic list)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Remove duplicates while preserving order
        unique_keywords = []
        seen = set()
        for keyword in keywords:
            if keyword not in seen:
                unique_keywords.append(keyword)
                seen.add(keyword)
        
        return unique_keywords[:max_keywords]
        
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []