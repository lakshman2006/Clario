from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import os
import sys
from datetime import datetime
from app.ml.recommender import LearningResourceRecommender
from app.utils.db_utils import DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/system", tags=["System"])

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        Health status information
    """
    try:
        return {
            "status": "success",
            "message": "System is healthy",
            "data": {
                "timestamp": datetime.utcnow().isoformat(),
                "service": "Clario Backend",
                "version": "1.0.0"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        raise HTTPException(
            status_code=500,
            detail="Health check failed"
        )

@router.get("/status")
async def system_status():
    """
    Detailed system status endpoint.
    
    Returns:
        Detailed system status information
    """
    try:
        status_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Clario Backend",
            "version": "1.0.0",
            "python_version": sys.version,
            "environment": {
                "debug": os.getenv("DEBUG", "False").lower() == "true",
                "database_url": os.getenv("DATABASE_URL", "app/data/clario.db")
            }
        }
        
        # Check database connection
        try:
            db = DatabaseManager()
            db.execute_query("SELECT 1")
            status_info["database"] = {"status": "connected", "error": None}
        except Exception as e:
            status_info["database"] = {"status": "error", "error": str(e)}
        
        # Check ML system
        try:
            recommender = LearningResourceRecommender()
            if recommender.initialize():
                status_info["ml_system"] = {"status": "ready", "error": None}
            else:
                status_info["ml_system"] = {"status": "error", "error": "Failed to initialize ML system"}
        except Exception as e:
            status_info["ml_system"] = {"status": "error", "error": str(e)}
        
        return {
            "status": "success",
            "message": "System status retrieved successfully",
            "data": status_info
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get system status"
        )

@router.get("/metrics")
async def system_metrics():
    """
    Basic system metrics endpoint.
    
    Returns:
        System metrics information
    """
    try:
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": "N/A",  # Could be calculated if needed
            "memory_usage": "N/A",  # Could be implemented if needed
            "disk_usage": "N/A",  # Could be implemented if needed
            "active_connections": "N/A"  # Could be implemented if needed
        }
        
        return {
            "status": "success",
            "message": "System metrics retrieved successfully",
            "data": metrics
        }
        
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get system metrics"
        )
