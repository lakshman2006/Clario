try:
    from jose import jwt
except ImportError:
    import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import requests
from app.config import settings
from app.utils.db_utils import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """
    Handles authentication using Google OAuth2 and JWT tokens.
    """
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_access_token(self, user_id: int, email: str, role: str = "user") -> str:
        """
        Create a JWT access token.
        
        Args:
            user_id: User ID
            email: User email
            role: User role
            
        Returns:
            JWT access token
        """
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    def get_google_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from Google using access token.
        
        Args:
            access_token: Google access token
            
        Returns:
            User information dictionary or None if failed
        """
        try:
            url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting Google user info: {e}")
            return None
    
    def get_google_authorization_url(self) -> str:
        """
        Get Google OAuth2 authorization URL.
        
        Returns:
            Google authorization URL
        """
        # Check if Google OAuth is properly configured
        if not settings.validate_google_oauth():
            logger.warning("Google OAuth not configured. Using test mode.")
            # Return a test URL that will show a message
            return "http://localhost:8000/api/v1/auth/test-login"
        
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline"
        }
        
        param_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{base_url}?{param_string}"
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from Google
            
        Returns:
            Token response or None if failed
        """
        try:
            url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}")
            return None
    
    def authenticate_user(self, google_user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate user and create or update user record.
        
        Args:
            google_user_info: User information from Google
            
        Returns:
            Authentication result with user info and access token
        """
        try:
            google_id = google_user_info.get("id")
            email = google_user_info.get("email")
            name = google_user_info.get("name")
            picture = google_user_info.get("picture")
            
            if not all([google_id, email, name]):
                raise ValueError("Missing required user information from Google")
            
            # Check if user exists
            user = self.db.get_user_by_google_id(google_id)
            
            if not user:
                # Create new user
                user_id = self.db.create_user(
                    google_id=google_id,
                    email=email,
                    name=name,
                    picture=picture
                )
                user = self.db.get_user_by_google_id(google_id)
                logger.info(f"Created new user: {email}")
            else:
                # Update existing user info
                self.db.update_user(
                    user["id"],
                    email=email,
                    name=name,
                    picture=picture
                )
                logger.info(f"Updated existing user: {email}")
            
            # Create JWT access token
            access_token = self.create_access_token(
                user_id=user["id"],
                email=user["email"],
                role=user.get("role", "user")
            )
            
            return {
                "user": user,
                "access_token": access_token,
                "token_type": "bearer"
            }
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            raise
    
    def logout_user(self, access_token: str) -> bool:
        """
        Logout user by invalidating the token.
        
        Args:
            access_token: JWT access token
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # For JWT tokens, we can't invalidate them server-side
            # In a production system, you might want to maintain a blacklist
            # For now, we'll just log the logout event
            self.db.log_event("user_logout")
            return True
            
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return False
    
    def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get current user from JWT token.
        
        Args:
            token: JWT access token
            
        Returns:
            User information or None if invalid token
        """
        try:
            payload = self.verify_token(token)
            if not payload:
                return None
            
            user_id = int(payload.get("sub"))
            user = self.db.execute_query("SELECT * FROM users WHERE id = ?", (user_id,))
            
            return user[0] if user else None
            
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            return None