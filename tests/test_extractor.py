import pytest
from unittest.mock import Mock
from src.extractor import extract_transcript
from youtube_transcript_api._errors import TranscriptsDisabled

def test_extract_transcript_success(mocker):
    """Test successful transcript extraction"""
    # Mock API response
    mock_transcript = [
        {'text': 'Hello', 'start': 0.0, 'duration': 1.5},
        {'text': 'world', 'start': 2.0, 'duration': 1.0}
    ]
    mock_api = mocker.patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript')
    mock_api.return_value = mock_transcript

    # Test valid URL
    url = "https://www.youtube.com/watch?v=abc123"
    result = extract_transcript(url)
    
    # Verify results
    assert result == "Hello world"
    mock_api.assert_called_once_with('abc123')

def test_extract_transcript_api_error(mocker):
    """Test error handling for disabled transcripts"""
    # Mock API exception
    mock_api = mocker.patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript')
    mock_api.side_effect = TranscriptsDisabled('video_id')  # Remove language parameter
    
    # Rest of test remains unchanged
    url = "https://youtu.be/xyz789"
    result = extract_transcript(url)
    
    assert result == "Error: Transcript is disabled for this video"
    mock_api.assert_called_once_with('xyz789')
