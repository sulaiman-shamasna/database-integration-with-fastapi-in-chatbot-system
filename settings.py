from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional
import os


class AppSettings(BaseSettings):
    """Application settings with environment variable support and validation."""
    
    # Application settings
    app_name: str = Field(default="Chatbot Application", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database settings - prefer DATABASE_URL, fallback to individual components
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="ChatbotApplicationDatabase", env="DB_NAME")
    db_user: str = Field(default="postgres", env="DB_USER")
    db_password: str = Field(default="", env="DB_PASSWORD")
    
    # OpenAI settings
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # (Removed vector DB features) Left intentionally blank to reflect current scope
    
    @validator('openai_api_key')
    def validate_openai_api_key(cls, v):
        if not v:
            raise ValueError("OPENAI_API_KEY is required")
        return v
    
    @validator('db_password')
    def validate_db_password(cls, v, values):
        # Only require password if using individual DB components
        if not values.get('database_url') and not v:
            raise ValueError("DB_PASSWORD is required when not using DATABASE_URL")
        return v
    
    @property
    def constructed_database_url(self) -> str:
        """Get database URL, constructing from components if needed."""
        if self.database_url:
            return self.database_url
        
        # Ensure password is properly handled
        password_part = f":{self.db_password}@" if self.db_password else "@"
        return f"postgresql+asyncpg://{self.db_user}{password_part}{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def pg_dsn(self) -> str:
        """Get synchronous PostgreSQL DSN for Alembic."""
        db_url = self.constructed_database_url
        # Convert asyncpg to psycopg2 for Alembic
        if "asyncpg" in db_url:
            return db_url.replace("asyncpg", "psycopg2")
        return db_url
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug and os.getenv("ENVIRONMENT", "").lower() == "production"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow extra fields from environment for flexibility
        extra = "ignore" 