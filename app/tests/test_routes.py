"""
Unit tests for API routes.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns healthy status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestAskEndpoint:
    """Test the ask question endpoint."""
    
    def test_ask_with_valid_video_url(self):
        """
        Test the ask endpoint with a valid YouTube URL.

        This test will fail with a 401 status code if the OpenRouter API key is not configured.
        However, the structure of the response should be valid if the API key is configured correctly.
        """
        payload = {
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "question": "What is this video about?"
        }
        response = client.post("/ask", json=payload)
        assert response.status_code == 200
    
    
    def test_ask_with_short_url(self):
        """Test ask endpoint with youtu.be short URL."""
        payload = {
            "video_url": "https://youtu.be/dQw4w9WgXcQ",
            "question": "Summarize this video"
        }
        response = client.post("/ask", json=payload)
        assert response.status_code == 200
    
