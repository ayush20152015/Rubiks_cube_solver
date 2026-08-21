import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration"""
    
    # API
    API_TITLE: str = "Rubik's Cube Solver API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Model paths
    MODEL_DIR: str = os.path.join(os.path.dirname(__file__), "../models")
    CNN_MODEL_PATH: str = os.path.join(MODEL_DIR, "face_classifier.h5")
    
    # ML settings
    IMAGE_SIZE: int = 224
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Cube solver
    SOLVER_TYPE: str = "ida_star"  # ida_star or bfs

    # Authentication
    AUTH_JWT_SECRET: str = "change-this-before-production"
    AUTH_JWT_EXPIRES_MINUTES: int = 1440
    USER_DATABASE_PATH: str = os.path.join(os.path.dirname(__file__), "data", "users.sqlite3")

    # Optional monitoring providers
    SENTRY_DSN: str = ""
    NEW_RELIC_CONFIG_FILE: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
