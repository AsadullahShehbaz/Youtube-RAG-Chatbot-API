# YouTube RAG Chatbot API

A production-grade FastAPI application that uses Retrieval-Augmented Generation (RAG) to answer questions about YouTube video content.

## Features

- 🎥 Fetch transcripts from YouTube videos
- 🔍 Semantic search using FAISS vector store
- 🤖 LLM-powered answer generation
- 📦 Modular, production-ready architecture
- 🚀 FastAPI with automatic API documentation
- ✅ Input validation with Pydantic

## Project Structure

```
youtube_rag_chatbot/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── api/routes.py           # API endpoints
│   ├── core/config.py          # Configuration
│   ├── models/schemas.py       # Request/response models
│   ├── services/
│   │   ├── transcript_service.py
│   │   ├── vectorstore_service.py
│   │   └── llm_service.py
│   └── utils/helpers.py
├── .env
├── requirements.txt
└── README.md
```

## Quick Commands

```bash
# Run tests
make test

# Run tests with coverage
make test-cov

# Run locally
make run

# Docker commands
make docker-build
make docker-run
make docker-logs
make docker-stop

# Clean cache
make clean
```

## Installation

1. **Clone and navigate to the project:**
```bash
cd youtube_rag_chatbot
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

## Usage

### Start the server:
```bash
python -m app.main
# Or use uvicorn directly:
uvicorn app.main:app --reload
```

### API Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example Request:
```bash
# Using full YouTube URL
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "question": "What is the main topic of this video?"
  }'

# Or using just the video ID
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "dQw4w9WgXcQ",
    "question": "What is the main topic of this video?"
  }'

# Works with youtu.be short links too!
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://youtu.be/dQw4w9WgXcQ",
    "question": "What is the main topic of this video?"
  }'
```

### Example Response:
```json
{
  "answer": "Based on the video content...",
  "video_id": "dQw4w9WgXcQ"
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health check |
| POST | `/ask` | Ask question about video |

## Architecture

### Services Layer:
- **TranscriptService**: Fetches YouTube transcripts
- **VectorStoreService**: Creates embeddings and vector stores
- **LLMService**: Generates answers using LLM

### Configuration:
All settings centralized in `config.py` for easy modification.

### Error Handling:
Comprehensive error handling with meaningful HTTP status codes.

## Interview Tips

**Key Points to Mention:**

1. **Modular Design**: Separated concerns (services, routes, config)
2. **Production Ready**: Error handling, validation, documentation
3. **Scalability**: Services can be easily cached or made async
4. **Maintainability**: Clear structure, easy to extend
5. **Best Practices**: Type hints, docstrings, configuration management

**Possible Improvements to Discuss:**

- Add caching for vector stores (Redis)
- Implement async operations for better performance
- Add rate limiting and authentication
- Deploy with Docker/Kubernetes
- Add monitoring and logging
- Implement batch processing for multiple videos

## License

MIT