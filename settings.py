from pydantic_settings import BaseSettings
from typing import Optional


class AppSettings(BaseSettings):
    # Database settings from environment variables
    database_url: Optional[str] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "ChatbotApplicationDatabase"
    db_user: str = "postgres"
    db_password: str = "*******"
    
    @property
    def constructed_database_url(self) -> str:
        """Construct database URL from individual components if not provided"""
        if self.database_url:
            return self.database_url
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    # For Alembic compatibility - create a synchronous URL
    @property
    def pg_dsn(self) -> str:
        """Return synchronous PostgreSQL DSN for Alembic"""
        db_url = self.constructed_database_url
        # Convert asyncpg to psycopg2 for Alembic
        if "asyncpg" in db_url:
            return db_url.replace("asyncpg", "psycopg2")
        return db_url
    
    # Optional: Add other settings as needed
    app_name: str = "Chatbot Application"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False 