"""
Configuration management for the application.
Loads environment variables and provides centralized config access.
"""
import os
from dotenv import load_dotenv
from app.core.logging_config import logger

# Load environment variables from .env
load_dotenv()
logger.debug(".env file loaded successfully")


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Model Configuration
    LLM_MODEL: str = "openai/gpt-oss-120b"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en"
    
    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVER_K: int = 3
    
    # API Configuration
    APP_TITLE: str = "YouTube RAG Chatbot API"
    APP_VERSION: str = "1.0.0"
    
    # Proxy Configuration
    PROXY_USERNAME: str = os.getenv("PROXY_USERNAME", "")
    PROXY_PASSWORD: str = os.getenv("PROXY_PASSWORD", "")

    def validate(self):
        """Validate required settings are present."""
        logger.debug("Validating application settings...")
        if not self.GROQ_API_KEY:
            logger.error("Validation failed: GROQ_API_KEY is missing in environment variables")
            raise ValueError("GROQ_API_KEY is required in .env file")
        logger.info("Settings validation successful")
        return True


# Global settings instance
settings = Settings()
try:
    settings.validate()
    logger.info(
        f"Configuration loaded: APP_TITLE='{settings.APP_TITLE}', "
        f"APP_VERSION='{settings.APP_VERSION}', "
        f"LLM_MODEL='{settings.LLM_MODEL}', "
        f"EMBEDDING_MODEL='{settings.EMBEDDING_MODEL}', "
        f"CHUNK_SIZE={settings.CHUNK_SIZE}, "
        f"CHUNK_OVERLAP={settings.CHUNK_OVERLAP}, "
        f"RETRIEVER_K={settings.RETRIEVER_K}"
    )
except Exception as e:
    logger.critical(f"Application failed to start due to configuration error: {e}")
    raise
