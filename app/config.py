import os
from typing import Optional

class Settings:
    """Application configuration settings."""
    
    # Application
    APP_NAME: str = "Clario Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "app/data/clario.db")
    
    # ML Settings
    ML_DATA_DIR: str = os.getenv("ML_DATA_DIR", "app/ml/data")
    ML_MODEL_DIR: str = os.getenv("ML_MODEL_DIR", "app/ml/model")
    
    # Google OAuth2
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/google/callback")
    
    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Clario"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",  # Vite dev server
        "https://localhost:3000",
        "https://localhost:8080",
    ]
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get database URL with proper formatting."""
        if cls.DATABASE_URL.startswith("sqlite"):
            return cls.DATABASE_URL
        else:
            return f"sqlite:///{cls.DATABASE_URL}"
    
    @classmethod
    def validate_google_oauth(cls) -> bool:
        """Validate that Google OAuth credentials are set."""
        return bool(cls.GOOGLE_CLIENT_ID and cls.GOOGLE_CLIENT_SECRET)

# Create settings instance
settings = Settings()
