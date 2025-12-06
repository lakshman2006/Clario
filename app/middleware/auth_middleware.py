from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from app.services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

# Security scheme for Swagger UI
security = HTTPBearer()

class AuthMiddleware:
    """
    Authentication middleware for protecting routes.
    """
    
    def __init__(self):
        self.auth_service = AuthService()
    
    async def get_current_user(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Dict[str, Any]:
        """
        Get current authenticated user from JWT token.
        
        Args:
            credentials: HTTP Bearer token credentials
            
        Returns:
            Current user information
            
        Raises:
            HTTPException: If token is invalid or user not found
        """
        try:
            token = credentials.credentials
            user = self.auth_service.get_current_user(token)
            
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in authentication middleware: {e}")
            raise HTTPException(
                status_code=401,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def get_current_user_optional(
        self, 
        request: Request
    ) -> Optional[Dict[str, Any]]:
        """
        Get current user if token is provided, otherwise return None.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Current user information or None
        """
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            token = auth_header.split(" ")[1]
            user = self.auth_service.get_current_user(token)
            
            return user
            
        except Exception as e:
            logger.warning(f"Optional authentication failed: {e}")
            return None
    
    def require_role(self, required_role: str):
        """
        Create a dependency that requires a specific role.
        
        Args:
            required_role: Required user role
            
        Returns:
            Dependency function
        """
        async def role_checker(current_user: Dict[str, Any] = Depends(self.get_current_user)):
            user_role = current_user.get("role", "user")
            
            if user_role != required_role and user_role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail=f"Insufficient permissions. Required role: {required_role}"
                )
            
            return current_user
        
        return role_checker

# Global auth middleware instance
auth_middleware = AuthMiddleware()

# Common dependencies
get_current_user = auth_middleware.get_current_user
get_current_user_optional = auth_middleware.get_current_user_optional
require_admin = auth_middleware.require_role("admin")