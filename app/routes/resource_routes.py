from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.utils.db_utils import DatabaseManager
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/resources", tags=["Resource Management"])
db = DatabaseManager()

# Pydantic models for request/response validation
class ResourceRequest(BaseModel):
    title: str
    description: Optional[str] = None
    type: str = "video"
    url: Optional[str] = None
    difficulty_level: int = 1
    estimated_hours: float = 1.0
    tags: Optional[str] = None

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    type: str
    url: Optional[str]
    difficulty_level: int
    estimated_hours: float
    tags: Optional[str]
    is_active: bool
    created_at: str

@router.get("/", response_model=Dict[str, Any])
async def get_all_resources(
    active_only: bool = Query(True, description="Only return active resources"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    difficulty_level: Optional[int] = Query(None, description="Filter by difficulty level")
):
    """
    Get all learning resources with optional filtering.
    
    Args:
        active_only: Only return active resources
        resource_type: Filter by resource type (video, article, course)
        difficulty_level: Filter by difficulty level (1-5)
        
    Returns:
        List of learning resources
    """
    try:
        if resource_type:
            resources = db.get_resources_by_type(resource_type)
        elif difficulty_level:
            resources = db.get_resources_by_difficulty(difficulty_level)
        else:
            resources = db.get_all_resources(active_only=active_only)
        
        return {
            "status": "success",
            "message": "Resources retrieved successfully",
            "data": resources,
            "count": len(resources)
        }
        
    except Exception as e:
        logger.error(f"Error getting resources: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get resources: {str(e)}")

@router.get("/types", response_model=Dict[str, Any])
async def get_resource_types():
    """
    Get all available resource types.
    
    Returns:
        List of resource types
    """
    try:
        resources = db.get_all_resources(active_only=True)
        types = list(set(resource['type'] for resource in resources))
        
        return {
            "status": "success",
            "message": "Resource types retrieved successfully",
            "data": {
                "types": types,
                "count": len(types)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting resource types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get resource types: {str(e)}")

@router.get("/difficulty-levels", response_model=Dict[str, Any])
async def get_difficulty_levels():
    """
    Get all available difficulty levels.
    
    Returns:
        List of difficulty levels
    """
    try:
        resources = db.get_all_resources(active_only=True)
        levels = sorted(list(set(resource['difficulty_level'] for resource in resources)))
        
        return {
            "status": "success",
            "message": "Difficulty levels retrieved successfully",
            "data": {
                "levels": levels,
                "count": len(levels)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting difficulty levels: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get difficulty levels: {str(e)}")

@router.post("/", response_model=Dict[str, Any])
async def create_resource(resource_data: ResourceRequest):
    """
    Create a new learning resource.
    
    Args:
        resource_data: Resource information
        
    Returns:
        Created resource information
    """
    try:
        resource_id = db.create_resource(
            title=resource_data.title,
            description=resource_data.description,
            type=resource_data.type,
            url=resource_data.url,
            difficulty_level=resource_data.difficulty_level,
            estimated_hours=resource_data.estimated_hours,
            tags=resource_data.tags
        )
        
        # Get the created resource
        resources = db.get_all_resources(active_only=False)
        created_resource = next((resource for resource in resources if resource['id'] == resource_id), None)
        
        if not created_resource:
            raise HTTPException(status_code=500, detail="Failed to retrieve created resource")
        
        return {
            "status": "success",
            "message": "Resource created successfully",
            "data": created_resource
        }
        
    except Exception as e:
        logger.error(f"Error creating resource: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create resource: {str(e)}")

@router.get("/{resource_id}", response_model=Dict[str, Any])
async def get_resource(resource_id: int):
    """
    Get a specific resource by ID.
    
    Args:
        resource_id: ID of the resource
        
    Returns:
        Resource information
    """
    try:
        resources = db.execute_query(
            "SELECT * FROM resources WHERE id = ?", 
            (resource_id,)
        )
        
        if not resources:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        return {
            "status": "success",
            "message": "Resource retrieved successfully",
            "data": resources[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting resource: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get resource: {str(e)}")

@router.put("/{resource_id}", response_model=Dict[str, Any])
async def update_resource(
    resource_id: int,
    resource_data: ResourceRequest
):
    """
    Update a resource.
    
    Args:
        resource_id: ID of the resource to update
        resource_data: Updated resource information
        
    Returns:
        Updated resource information
    """
    try:
        update_data = {
            "title": resource_data.title,
            "description": resource_data.description,
            "type": resource_data.type,
            "url": resource_data.url,
            "difficulty_level": resource_data.difficulty_level,
            "estimated_hours": resource_data.estimated_hours,
            "tags": resource_data.tags
        }
        
        rows_affected = db.update_resource(resource_id, **update_data)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        # Get updated resource
        resources = db.execute_query(
            "SELECT * FROM resources WHERE id = ?", 
            (resource_id,)
        )
        
        return {
            "status": "success",
            "message": "Resource updated successfully",
            "data": resources[0] if resources else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating resource: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update resource: {str(e)}")

@router.delete("/{resource_id}", response_model=Dict[str, Any])
async def delete_resource(resource_id: int):
    """
    Delete a resource (soft delete by setting is_active to False).
    
    Args:
        resource_id: ID of the resource to delete
        
    Returns:
        Deletion confirmation
    """
    try:
        rows_affected = db.update_resource(resource_id, is_active=False)
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        return {
            "status": "success",
            "message": "Resource deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resource: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete resource: {str(e)}")

@router.get("/search/{query}", response_model=Dict[str, Any])
async def search_resources(
    query: str,
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    difficulty_level: Optional[int] = Query(None, description="Filter by difficulty level")
):
    """
    Search resources by title or description.
    
    Args:
        query: Search query
        resource_type: Filter by resource type
        difficulty_level: Filter by difficulty level
        
    Returns:
        List of matching resources
    """
    try:
        search_query = f"%{query}%"
        sql_query = """
            SELECT * FROM resources 
            WHERE (title LIKE ? OR description LIKE ?) AND is_active = 1
        """
        params = [search_query, search_query]
        
        if resource_type:
            sql_query += " AND type = ?"
            params.append(resource_type)
        
        if difficulty_level:
            sql_query += " AND difficulty_level = ?"
            params.append(difficulty_level)
        
        sql_query += " ORDER BY title"
        
        resources = db.execute_query(sql_query, tuple(params))
        
        return {
            "status": "success",
            "message": "Search completed successfully",
            "data": resources,
            "count": len(resources),
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Error searching resources: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search resources: {str(e)}")
