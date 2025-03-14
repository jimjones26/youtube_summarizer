from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import youtube_dl
from urllib.parse import urlparse, parse_qs

def extract_transcript(url: str) -> str:
    """Extract and concatenate YouTube video transcript."""
    try:
        # Extract video ID from different URL formats
        if 'youtu.be' in url:
            video_id = urlparse(url).path.lstrip('/')
        else:
            query = urlparse(url).query
            video_id = parse_qs(query).get('v', [None])[0]
        
        if not video_id:
            return "Error: Invalid YouTube URL"
        
        # Retrieve transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join(entry['text'] for entry in transcript)
    
    except TranscriptsDisabled:
        return "Error: Transcript is disabled for this video"

def get_video_metadata(url):
    """
    Fetch metadata for a YouTube video using youtube_dl.
    Returns a dictionary with title, duration, upload_date, uploader, etc.
    """
    ydl_opts = {'quiet': True}  # Suppress console output
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # Fetch info without downloading
        return info