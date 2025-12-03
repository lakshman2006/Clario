from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.schemas.ml_schema import RecommendationRequest, RecommendationResponse, ErrorResponse
from app.ml.recommender import LearningResourceRecommender
from app.middleware.auth_middleware import get_current_user_optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ml", tags=["ML"])

# Initialize the recommender
recommender = LearningResourceRecommender()

@router.on_event("startup")
async def startup_event():
    """Initialize the ML recommender on startup."""
    try:
        success = recommender.initialize()
        if success:
            logger.info("ML Recommender initialized successfully")
        else:
            logger.error("Failed to initialize ML Recommender")
    except Exception as e:
        logger.error(f"Error during ML Recommender initialization: {e}")

@router.get("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    topic: str = Query(..., description="Topic for which to get recommendations"),
    top_k: int = Query(5, ge=1, le=10, description="Number of recommendations to return"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type (video, article, course)")
):
    """
    Get learning resource recommendations based on a topic.
    
    Args:
        topic: The topic of interest
        top_k: Number of recommendations to return (1-10)
        resource_type: Optional filter by resource type
        
    Returns:
        List of recommended learning resources
    """
    try:
        if not topic.strip():
            raise HTTPException(
                status_code=400,
                detail="Topic cannot be empty"
            )
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            topic=topic,
            top_k=top_k,
            filter_type=resource_type
        )
        
        if not recommendations:
            return RecommendationResponse(
                status="success",
                message="No recommendations found for the given topic",
                data=[]
            )
        
        return RecommendationResponse(
            status="success",
            message="Recommendations fetched successfully",
            data=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/recommendations/by-type", response_model=dict)
async def get_recommendations_by_type(
    topic: str = Query(..., description="Topic for which to get recommendations"),
    top_k: int = Query(3, ge=1, le=5, description="Number of recommendations per type")
):
    """
    Get learning resource recommendations categorized by type.
    
    Args:
        topic: The topic of interest
        top_k: Number of recommendations per type (1-5)
        
    Returns:
        Dictionary with resource types as keys and recommendations as values
    """
    try:
        if not topic.strip():
            raise HTTPException(
                status_code=400,
                detail="Topic cannot be empty"
            )
        
        # Get recommendations by type
        recommendations_by_type = recommender.get_recommendations_by_type(
            topic=topic,
            top_k=top_k
        )
        
        return {
            "status": "success",
            "message": "Recommendations fetched successfully by type",
            "data": recommendations_by_type
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendations by type: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/resource-types", response_model=dict)
async def get_resource_types():
    """
    Get all available resource types.
    
    Returns:
        List of available resource types
    """
    try:
        resource_types = recommender.get_all_resource_types()
        
        return {
            "status": "success",
            "message": "Resource types fetched successfully",
            "data": {
                "types": resource_types,
                "count": len(resource_types)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting resource types: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations_post(request: RecommendationRequest):
    """
    Get learning resource recommendations using POST method.
    
    Args:
        request: Recommendation request with topic
        
    Returns:
        List of recommended learning resources
    """
    try:
        if not request.topic.strip():
            raise HTTPException(
                status_code=400,
                detail="Topic cannot be empty"
            )
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            topic=request.topic,
            top_k=5  # Default to 5 recommendations
        )
        
        if not recommendations:
            return RecommendationResponse(
                status="success",
                message="No recommendations found for the given topic",
                data=[]
            )
        
        return RecommendationResponse(
            status="success",
            message="Recommendations fetched successfully",
            data=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
