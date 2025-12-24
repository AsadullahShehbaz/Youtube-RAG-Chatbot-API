"""
API routes for the YouTube RAG chatbot.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, HealthResponse
from app.services.transcript_service import TranscriptService
from app.services.vectorstore_service import VectorStoreService
from app.services.llm_service import LLMService

# Create router
router = APIRouter()

# Initialize services (singleton pattern)
transcript_service = TranscriptService()
vectorstore_service = VectorStoreService()
llm_service = LLMService()


@router.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        message="YouTube RAG Chatbot API is running"
    )


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="All systems operational"
    )


@router.post("/ask", response_model=QueryResponse, tags=["Chat"])
async def ask_question(payload: QueryRequest):
    """
    Ask a question about a YouTube video.
    
    This endpoint:
    1. Extracts video ID from URL (or accepts direct video ID)
    2. Fetches the transcript from YouTube
    3. Creates a vector store from the transcript
    4. Retrieves relevant context for the question
    5. Generates an answer using LLM
    
    Args:
        payload: QueryRequest containing video_url (URL or ID) and question
    
    Returns:
        QueryResponse with the generated answer
    """
    try:
        # video_url is already validated and converted to video_id by Pydantic
        video_url = payload.video_url
        
        # Step 1: Fetch transcript
        transcript = transcript_service.fetch_transcript(video_url)
        print(f'Step 1 Fetch transcript completed : {transcript}')
        # Step 2: Create vector store
        vectorstore = vectorstore_service.create_vectorstore(transcript)
        print(f"Step 2 Create vector store completed {vectorstore}")
        # Step 3: Retrieve relevant documents
        retrieved_docs = vectorstore_service.retrieve_documents(
            vectorstore,
            payload.question
        )
        print(f"Step 3 completed: Retrieve relevant documents")
        # Step 4: Format context and generate answer
        context = llm_service.format_documents(retrieved_docs)
        answer = llm_service.generate_answer(context, payload.question)
        print(f"Step 4 completed: Format context and generate answer")
        return QueryResponse(
            answer=answer,
            video_url=video_url
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions from services
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )