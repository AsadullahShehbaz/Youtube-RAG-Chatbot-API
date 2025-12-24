"""
Service for fetching and processing YouTube transcripts.
"""
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from fastapi import HTTPException
from app.utils.helpers import extract_video_id_from_url

class TranscriptService:
    """Handles YouTube transcript fetching and processing."""
    
    def __init__(self):
        self.api = YouTubeTranscriptApi()
    
    def fetch_transcript(self, video_url: str, languages: list = None) -> str:
        """
        Fetch transcript for a YouTube video.
        
        Args:
            video_URL: YouTube video URL
            languages: List of language codes to try (default: ['en', 'hi'])
        
        Returns:
            Combined transcript text
        
        Raises:
            HTTPException: If transcript cannot be fetched
        """
        if languages is None:
            languages = ['en', 'hi','ur']
        
        try:
            video_id = extract_video_id_from_url(video_url)
            transcript_obj = self.api.fetch(video_id, languages=languages)
            transcript = " ".join(snippet.text for snippet in transcript_obj.snippets)
            
            if not transcript.strip():
                raise HTTPException(
                    status_code=404,
                    detail="Transcript is empty for this video"
                )
            
            return transcript
            
        except TranscriptsDisabled:
            raise HTTPException(
                status_code=404,
                detail="Transcripts are disabled for this video"
            )
        except NoTranscriptFound:
            raise HTTPException(
                status_code=404,
                detail=f"No transcript found in languages: {', '.join(languages)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error fetching transcript: {str(e)}"
            )