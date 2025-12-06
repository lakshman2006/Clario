from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from typing import Dict, Any
from app.services.auth_service import AuthService
from app.utils.db_utils import DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
auth_service = AuthService()
db = DatabaseManager()

@router.get("/test-login")
async def test_login():
    """
    Test login endpoint for development when Google OAuth is not configured.
    Creates a test user and returns a JWT token.
    """
    try:
        # Create a test user
        test_user_data = {
            "google_id": "test_user_123",
            "email": "test@clario.com",
            "name": "Test User",
            "picture": "https://via.placeholder.com/150"
        }
        
        # Check if test user exists
        existing_user = db.get_user_by_google_id("test_user_123")
        
        if not existing_user:
            # Create test user
            user_id = db.create_user(**test_user_data)
            logger.info(f"Created test user with ID: {user_id}")
        else:
            user_id = existing_user["id"]
            logger.info(f"Using existing test user with ID: {user_id}")
        
        # Create JWT token
        access_token = auth_service.create_access_token(
            user_id=user_id,
            email=test_user_data["email"],
            role="user"
        )
        
        return {
            "status": "success",
            "message": "Test login successful",
            "data": {
                "user": {
                    "id": user_id,
                    "email": test_user_data["email"],
                    "name": test_user_data["name"],
                    "picture": test_user_data["picture"]
                },
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in test login: {e}")
        raise HTTPException(
            status_code=500,
            detail="Test login failed"
        )

@router.get("/google/login")
async def google_login():
    """
    Initiate Google OAuth2 login flow.
    
    Returns:
        Redirect to Google authorization page
    """
    try:
        auth_url = auth_service.get_google_authorization_url()
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        logger.error(f"Error initiating Google login: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to initiate Google login"
        )

@router.get("/google/callback")
async def google_callback(code: str = None, error: str = None):
    """
    Handle Google OAuth2 callback.
    
    Args:
        code: Authorization code from Google
        error: Error message from Google
        
    Returns:
        Authentication result or error
    """
    try:
        if error:
            raise HTTPException(
                status_code=400,
                detail=f"Google OAuth error: {error}"
            )
        
        if not code:
            raise HTTPException(
                status_code=400,
                detail="Authorization code not provided"
            )
        
        # Exchange code for token
        token_response = auth_service.exchange_code_for_token(code)
        if not token_response:
            raise HTTPException(
                status_code=400,
                detail="Failed to exchange code for token"
            )
        
        access_token = token_response.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=400,
                detail="No access token received from Google"
            )
        
        # Get user info from Google
        google_user_info = auth_service.get_google_user_info(access_token)
        if not google_user_info:
            raise HTTPException(
                status_code=400,
                detail="Failed to get user information from Google"
            )
        
        # Authenticate user
        auth_result = auth_service.authenticate_user(google_user_info)
        
        # Log the login event
        db.log_event("user_login", ip_address="127.0.0.1")  # You might want to get real IP
        
        return {
            "status": "success",
            "message": "Authentication successful",
            "data": auth_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Google callback: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during authentication"
        )

@router.post("/logout")
async def logout(request: Request):
    """
    Logout user.
    
    Returns:
        Logout confirmation
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
        
        # Logout user
        success = auth_service.logout_user(token)
        
        if success:
            return {
                "status": "success",
                "message": "Logout successful"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to logout"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during logout"
        )

@router.get("/me")
async def get_current_user_info(request: Request):
    """
    Get current user information.
    
    Returns:
        Current user information
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
        
        return {
            "status": "success",
            "message": "User information retrieved successfully",
            "data": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "picture": user.get("picture"),
                "role": user.get("role", "user"),
                "created_at": user.get("created_at")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
