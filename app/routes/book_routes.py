"""
Book Recommendation API Routes

This module provides API endpoints for book recommendations.
Completely separate from the schedule maker functionality.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.ml.book_recommender import BookRecommender
from app.middleware.auth_middleware import get_current_user_optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/books", tags=["Book Recommendations"])

# Initialize the book recommender
book_recommender = BookRecommender()

@router.on_event("startup")
async def startup_event():
    """Initialize the book recommender on startup."""
    try:
        success = book_recommender.initialize()
        if success:
            logger.info("Book Recommender initialized successfully")
        else:
            logger.error("Failed to initialize Book Recommender")
    except Exception as e:
        logger.error(f"Error during Book Recommender initialization: {e}")

@router.get("/recommendations")
async def get_book_recommendations(
    topic: str = Query(..., description="Topic for which to get book recommendations"),
    top_k: int = Query(5, ge=1, le=20, description="Number of recommendations to return"),
    genre: Optional[str] = Query(None, description="Filter by genre (Programming, Computer Science, Machine Learning, etc.)"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty (Beginner, Intermediate, Advanced, Expert)"),
    min_rating: float = Query(0.0, ge=0.0, le=5.0, description="Minimum rating filter"),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get book recommendations based on a topic.
    
    This endpoint is completely separate from the schedule maker functionality.
    It focuses solely on recommending relevant books based on the input topic.
    
    Args:
        topic: The topic of interest (e.g., "machine learning", "python programming")
        top_k: Number of recommendations to return (1-20)
        genre: Optional filter by book genre
        difficulty_level: Optional filter by difficulty level
        min_rating: Minimum rating filter (0.0-5.0)
        
    Returns:
        List of recommended books with detailed information
    """
    try:
        if not topic.strip():
            raise HTTPException(
                status_code=400,
                detail="Topic cannot be empty"
            )
        
        logger.info(f"Getting book recommendations for topic: '{topic}'")
        
        # Get recommendations from the book recommender
        recommendations = book_recommender.get_book_recommendations(
            topic=topic,
            top_k=top_k,
            genre=genre,
            difficulty_level=difficulty_level,
            min_rating=min_rating
        )
        
        if not recommendations:
            return {
                "status": "success",
                "message": f"No book recommendations found for topic '{topic}'",
                "data": [],
                "total_recommendations": 0
            }
        
        return {
            "status": "success",
            "message": f"Found {len(recommendations)} book recommendations for topic '{topic}'",
            "data": recommendations,
            "total_recommendations": len(recommendations),
            "filters_applied": {
                "genre": genre,
                "difficulty_level": difficulty_level,
                "min_rating": min_rating
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting book recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get book recommendations: {str(e)}"
        )

@router.get("/search")
async def search_books(
    query: str = Query(..., description="Search query for books"),
    top_k: int = Query(10, ge=1, le=20, description="Number of results to return"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Search books by title, author, or description.
    
    Args:
        query: Search query (searches in title, author, description)
        top_k: Number of results to return (1-20)
        genre: Optional filter by genre
        
    Returns:
        List of matching books
    """
    try:
        if not query.strip():
            raise HTTPException(
                status_code=400,
                detail="Search query cannot be empty"
            )
        
        logger.info(f"Searching books with query: '{query}'")
        
        # Search books
        results = book_recommender.search_books(
            query=query,
            top_k=top_k,
            genre=genre
        )
        
        if not results:
            return {
                "status": "success",
                "message": f"No books found matching '{query}'",
                "data": [],
                "total_results": 0
            }
        
        return {
            "status": "success",
            "message": f"Found {len(results)} books matching '{query}'",
            "data": results,
            "total_results": len(results),
            "filters_applied": {
                "genre": genre
            }
        }
        
    except Exception as e:
        logger.error(f"Error searching books: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search books: {str(e)}"
        )

@router.get("/genres")
async def get_available_genres(
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get list of available book genres.
    
    Returns:
        List of available genres
    """
    try:
        if book_recommender.books_df is None:
            book_recommender.load_books_data()
        
        if book_recommender.books_df is None:
            return {
                "status": "success",
                "message": "No book data available",
                "data": []
            }
        
        genres = book_recommender.books_df['genre'].unique().tolist()
        genres.sort()
        
        return {
            "status": "success",
            "message": f"Found {len(genres)} available genres",
            "data": genres
        }
        
    except Exception as e:
        logger.error(f"Error getting genres: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get genres: {str(e)}"
        )

@router.get("/difficulty-levels")
async def get_difficulty_levels(
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get list of available difficulty levels.
    
    Returns:
        List of available difficulty levels
    """
    try:
        if book_recommender.books_df is None:
            book_recommender.load_books_data()
        
        if book_recommender.books_df is None:
            return {
                "status": "success",
                "message": "No book data available",
                "data": []
            }
        
        difficulty_levels = book_recommender.books_df['difficulty_level'].unique().tolist()
        difficulty_levels.sort()
        
        return {
            "status": "success",
            "message": f"Found {len(difficulty_levels)} difficulty levels",
            "data": difficulty_levels
        }
        
    except Exception as e:
        logger.error(f"Error getting difficulty levels: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get difficulty levels: {str(e)}"
        )

@router.get("/topics")
async def get_popular_topics(
    limit: int = Query(20, ge=1, le=50, description="Number of topics to return"),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get list of popular book topics.
    
    Returns:
        List of popular topics
    """
    try:
        if book_recommender.books_df is None:
            book_recommender.load_books_data()
        
        if book_recommender.books_df is None:
            return {
                "status": "success",
                "message": "No book data available",
                "data": []
            }
        
        # Get topic counts
        topic_counts = book_recommender.books_df['topic'].value_counts().head(limit)
        topics = topic_counts.index.tolist()
        
        return {
            "status": "success",
            "message": f"Found {len(topics)} popular topics",
            "data": topics
        }
        
    except Exception as e:
        logger.error(f"Error getting topics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get topics: {str(e)}"
        )
