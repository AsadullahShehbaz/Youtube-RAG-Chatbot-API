"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings
import warnings
from contextlib import asynccontextmanager
from app.core.logging_config import logger

# Suppress warnings
warnings.filterwarnings("ignore")

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(f"Starting {settings.APP_TITLE} v{settings.APP_VERSION}")
    yield
    # Shutdown logic
    logger.info("Shutting down application...")

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="A RAG-based chatbot for answering questions about YouTube video content",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.debug("CORS middleware configured with allow_origins='*'")

# Include routers
app.include_router(router)
logger.info("API routes included successfully")

if __name__ == "__main__":
    import uvicorn
    logger.info("Launching Uvicorn server on host=0.0.0.0 port=8000")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
