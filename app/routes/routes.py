from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Include route modules with error handling
try:
    from app.routes import ml_routes
    router.include_router(ml_routes.router)
    logger.info("ML routes loaded successfully")
except Exception as e:
    logger.warning(f"ML routes not loaded: {e}")

try:
    from app.routes import system_routes
    router.include_router(system_routes.router)
    logger.info("System routes loaded successfully")
except Exception as e:
    logger.warning(f"System routes not loaded: {e}")

try:
    from app.routes import auth_routes
    router.include_router(auth_routes.router)
    logger.info("Auth routes loaded successfully")
except Exception as e:
    logger.warning(f"Auth routes not loaded (missing dependencies): {e}")

try:
    from app.routes import user_routes
    router.include_router(user_routes.router)
    logger.info("User routes loaded successfully")
except Exception as e:
    logger.warning(f"User routes not loaded: {e}")

try:
    from app.routes import learning_routes
    router.include_router(learning_routes.router)
    logger.info("Learning routes loaded successfully")
except Exception as e:
    logger.warning(f"Learning routes not loaded: {e}")

try:
    from app.routes import resource_routes
    router.include_router(resource_routes.router)
    logger.info("Resource routes loaded successfully")
except Exception as e:
    logger.warning(f"Resource routes not loaded: {e}")

try:
    from app.routes import schedule_routes_simple as schedule_routes
    router.include_router(schedule_routes.router)
    logger.info("Schedule routes loaded successfully")
except Exception as e:
    logger.warning(f"Schedule routes not loaded: {e}")

try:
    from app.routes import book_routes
    router.include_router(book_routes.router)
    logger.info("Book recommendation routes loaded successfully")
except Exception as e:
    logger.warning(f"Book recommendation routes not loaded: {e}")
