"""
Configuration management for the application.
Loads environment variables and provides centralized config access.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Model Configuration
    LLM_MODEL: str = "openai/gpt-oss-120b"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVER_K: int = 3
    
    # API Configuration
    APP_TITLE: str = "YouTube RAG Chatbot API"
    APP_VERSION: str = "1.0.0"
    
    def validate(self):
        """Validate required settings are present."""
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required in .env file")
        return True


# Global settings instance
settings = Settings()
settings.validate()