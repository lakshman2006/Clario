#!/usr/bin/env python3
"""
Server runner script for Clario Backend
"""
import uvicorn
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.venv', 'app'))

if __name__ == "__main__":
    # Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    RELOAD = os.getenv("RELOAD", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
    
    print(f"Starting Clario Backend server...")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")
    print(f"Reload: {RELOAD}")
    print(f"Log Level: {LOG_LEVEL}")
    print(f"API Documentation: http://{HOST}:{PORT}/docs")
    print(f"Health Check: http://{HOST}:{PORT}/health")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level=LOG_LEVEL,
        access_log=True
    )
