from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any
from app.services.auth_service import AuthService
from app.utils.db_utils import DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
auth_service = AuthService()
db = DatabaseManager()

def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Current user information
        
    Raises:
        HTTPException: If user is not authenticated
    """
    try:
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authorization header missing or invalid"
            )
        
        token = auth_header.split(" ")[1]
        
        # Get current user
        user = auth_service.get_current_user(token)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/profile")
async def get_user_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current user's profile information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User profile information
    """
    try:
        return {
            "status": "success",
            "message": "User profile retrieved successfully",
            "data": {
                "id": current_user["id"],
                "email": current_user["email"],
                "name": current_user["name"],
                "picture": current_user.get("picture"),
                "role": current_user.get("role", "user"),
                "created_at": current_user.get("created_at")
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.put("/profile")
async def update_user_profile(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update current user's profile information.
    
    Args:
        request: FastAPI request object
        current_user: Current authenticated user
        
    Returns:
        Updated user profile information
    """
    try:
        # Get update data from request body
        update_data = await request.json()
        
        # Allowed fields for update
        allowed_fields = ["name", "picture"]
        filtered_data = {key: value for key, value in update_data.items() if key in allowed_fields}
        
        if not filtered_data:
            raise HTTPException(
                status_code=400,
                detail="No valid fields provided for update"
            )
        
        # Update user in database
        rows_affected = db.update_user(current_user["id"], **filtered_data)
        
        if rows_affected == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        # Get updated user data
        updated_user = db.execute_query("SELECT * FROM users WHERE id = ?", (current_user["id"],))[0]
        
        return {
            "status": "success",
            "message": "User profile updated successfully",
            "data": {
                "id": updated_user["id"],
                "email": updated_user["email"],
                "name": updated_user["name"],
                "picture": updated_user.get("picture"),
                "role": updated_user.get("role", "user"),
                "created_at": updated_user.get("created_at")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/preferences")
async def get_user_preferences(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current user's preferences.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User preferences
    """
    try:
        # For now, return default preferences
        # In the future, this could be stored in the database
        return {
            "status": "success",
            "message": "User preferences retrieved successfully",
            "data": {
                "preferred_resource_types": ["video", "article", "course"],
                "learning_goals": [],
                "time_preferences": {
                    "morning": True,
                    "afternoon": True,
                    "evening": True
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting user preferences: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.put("/preferences")
async def update_user_preferences(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update current user's preferences.
    
    Args:
        request: FastAPI request object
        current_user: Current authenticated user
        
    Returns:
        Updated user preferences
    """
    try:
        # Get preferences data from request body
        preferences_data = await request.json()
        
        # For now, just return the updated preferences
        # In the future, this could be stored in the database
        return {
            "status": "success",
            "message": "User preferences updated successfully",
            "data": preferences_data
        }
        
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
