def test_python_environment():
    # Check Python version (assuming we need at least 3.6)
    import sys
    assert sys.version_info >= (3, 6), "Python version must be 3.6 or higher"

    # Check for required libraries
    try:
        import youtube_transcript_api
    except ImportError:
        assert False, "youtube_transcript_api library not found"
    try:
        import requests
    except ImportError:
        assert False, "requests library not found"
    try:
        import pytest
    except ImportError:
        assert False, "pytest library not found"
