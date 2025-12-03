from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any, Optional
from app.utils.db_utils import DatabaseManager
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/learning", tags=["Learning Management"])
db = DatabaseManager()

# Pydantic models for request/response validation
class LearningGoalRequest(BaseModel):
    goal_title: str
    description: Optional[str] = None
    difficulty_level: int = 1
    target_hours: int = 10
    deadline: Optional[str] = None

class TimeAvailabilityRequest(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str
    is_available: bool = True

class LearningGoalResponse(BaseModel):
    id: int
    user_id: int
    goal_title: str
    description: Optional[str]
    difficulty_level: int
    target_hours: int
    deadline: Optional[str]
    status: str
    created_at: str

class TimeAvailabilityResponse(BaseModel):
    id: int
    user_id: int
    day_of_week: str
    start_time: str
    end_time: str
    is_available: bool
    created_at: str

# Helper function to get current user (placeholder for now)
def get_current_user_id(request: Request) -> int:
    """Get current user ID. For now, return a default user ID."""
    # TODO: Implement proper authentication
    return 1

@router.post("/goals", response_model=Dict[str, Any])
async def create_learning_goal(
    goal_data: LearningGoalRequest,
    request: Request
):
    """
    Create a new learning goal for the current user.
    
    Args:
        goal_data: Learning goal information
        request: FastAPI request object
        
    Returns:
        Created learning goal information
    """
    try:
        user_id = get_current_user_id(request)
        
        goal_id = db.create_learning_goal(
            user_id=user_id,
            goal_title=goal_data.goal_title,
            description=goal_data.description,
            difficulty_level=goal_data.difficulty_level,
            target_hours=goal_data.target_hours,
            deadline=goal_data.deadline
        )
        
        # Get the created goal
        goals = db.get_user_learning_goals(user_id)
        created_goal = next((goal for goal in goals if goal['id'] == goal_id), None)
        
        if not created_goal:
            raise HTTPException(status_code=500, detail="Failed to retrieve created goal")
        
        return {
            "status": "success",
            "message": "Learning goal created successfully",
            "data": created_goal
        }
        
    except Exception as e:
        logger.error(f"Error creating learning goal: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create learning goal: {str(e)}")

@router.get("/goals", response_model=Dict[str, Any])
async def get_learning_goals(request: Request):
    """
    Get all learning goals for the current user.
    
    Args:
        request: FastAPI request object
        
    Returns:
        List of learning goals
    """
    try:
        user_id = get_current_user_id(request)
        goals = db.get_user_learning_goals(user_id)
        
        return {
            "status": "success",
            "message": "Learning goals retrieved successfully",
            "data": goals,
            "count": len(goals)
        }
        
    except Exception as e:
        logger.error(f"Error getting learning goals: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get learning goals: {str(e)}")

@router.put("/goals/{goal_id}", response_model=Dict[str, Any])
async def update_learning_goal(
    goal_id: int,
    goal_data: LearningGoalRequest,
    request: Request
):
    """
    Update a learning goal.
    
    Args:
        goal_id: ID of the goal to update
        goal_data: Updated goal information
        request: FastAPI request object
        
    Returns:
        Updated learning goal information
    """
    try:
        user_id = get_current_user_id(request)
        
        # Update the goal
        update_data = {
            "goal_title": goal_data.goal_title,
            "description": goal_data.description,
            "difficulty_level": goal_data.difficulty_level,
            "target_hours": goal_data.target_hours,
            "deadline": goal_data.deadline
        }
        
        rows_affected = db.update_learning_goal(goal_id, **update_data)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Learning goal not found")
        
        # Get updated goal
        goals = db.get_user_learning_goals(user_id)
        updated_goal = next((goal for goal in goals if goal['id'] == goal_id), None)
        
        return {
            "status": "success",
            "message": "Learning goal updated successfully",
            "data": updated_goal
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating learning goal: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update learning goal: {str(e)}")

@router.delete("/goals/{goal_id}", response_model=Dict[str, Any])
async def delete_learning_goal(goal_id: int, request: Request):
    """
    Delete a learning goal.
    
    Args:
        goal_id: ID of the goal to delete
        request: FastAPI request object
        
    Returns:
        Deletion confirmation
    """
    try:
        rows_affected = db.delete_learning_goal(goal_id)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Learning goal not found")
        
        return {
            "status": "success",
            "message": "Learning goal deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting learning goal: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete learning goal: {str(e)}")

@router.post("/availability", response_model=Dict[str, Any])
async def set_time_availability(
    availability_data: TimeAvailabilityRequest,
    request: Request
):
    """
    Set time availability for the current user.
    
    Args:
        availability_data: Time availability information
        request: FastAPI request object
        
    Returns:
        Created time availability information
    """
    try:
        user_id = get_current_user_id(request)
        
        availability_id = db.set_time_availability(
            user_id=user_id,
            day_of_week=availability_data.day_of_week,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time,
            is_available=availability_data.is_available
        )
        
        # Get the created availability
        availability = db.get_user_time_availability(user_id)
        created_availability = next((avail for avail in availability if avail['id'] == availability_id), None)
        
        if not created_availability:
            raise HTTPException(status_code=500, detail="Failed to retrieve created availability")
        
        return {
            "status": "success",
            "message": "Time availability set successfully",
            "data": created_availability
        }
        
    except Exception as e:
        logger.error(f"Error setting time availability: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to set time availability: {str(e)}")

@router.get("/availability", response_model=Dict[str, Any])
async def get_time_availability(request: Request):
    """
    Get time availability for the current user.
    
    Args:
        request: FastAPI request object
        
    Returns:
        List of time availability
    """
    try:
        user_id = get_current_user_id(request)
        availability = db.get_user_time_availability(user_id)
        
        return {
            "status": "success",
            "message": "Time availability retrieved successfully",
            "data": availability,
            "count": len(availability)
        }
        
    except Exception as e:
        logger.error(f"Error getting time availability: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get time availability: {str(e)}")

@router.put("/availability/{availability_id}", response_model=Dict[str, Any])
async def update_time_availability(
    availability_id: int,
    availability_data: TimeAvailabilityRequest,
    request: Request
):
    """
    Update time availability.
    
    Args:
        availability_id: ID of the availability to update
        availability_data: Updated availability information
        request: FastAPI request object
        
    Returns:
        Updated time availability information
    """
    try:
        update_data = {
            "day_of_week": availability_data.day_of_week,
            "start_time": availability_data.start_time,
            "end_time": availability_data.end_time,
            "is_available": availability_data.is_available
        }
        
        rows_affected = db.update_time_availability(availability_id, **update_data)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Time availability not found")
        
        # Get updated availability
        updated_availability = db.execute_query(
            "SELECT * FROM time_availability WHERE id = ?", 
            (availability_id,)
        )
        
        return {
            "status": "success",
            "message": "Time availability updated successfully",
            "data": updated_availability[0] if updated_availability else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating time availability: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update time availability: {str(e)}")

@router.delete("/availability/{availability_id}", response_model=Dict[str, Any])
async def delete_time_availability(availability_id: int, request: Request):
    """
    Delete time availability.
    
    Args:
        availability_id: ID of the availability to delete
        request: FastAPI request object
        
    Returns:
        Deletion confirmation
    """
    try:
        rows_affected = db.delete_time_availability(availability_id)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Time availability not found")
        
        return {
            "status": "success",
            "message": "Time availability deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting time availability: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete time availability: {str(e)}")
