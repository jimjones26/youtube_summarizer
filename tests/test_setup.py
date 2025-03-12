import pytest

def test_required_libraries_available():
    try:
        import youtube_transcript_api
        import requests
        assert True  # Libraries imported successfully
    except ImportError as e:
        pytest.fail(f"One or more required libraries not found: {e}")
