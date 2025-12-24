"""
Utility helper functions.
"""
import re


def validate_youtube_id(video_id: str) -> bool:
    """
    Validate YouTube video ID format.
    
    Args:
        video_id: YouTube video ID
    
    Returns:
        True if valid format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9_-]{11}$'
    print(f'This video id is valid : {video_id}')
    return bool(re.match(pattern, video_id))


def extract_video_id_from_url(url: str) -> str:
    """
    Extract video ID from YouTube URL.
    
    Args:
        url: YouTube URL
    
    Returns:
        Video ID or empty string if not found
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            print(f"Video id is extracted from URL {url}")
            return match.group(1)
    
    return ""