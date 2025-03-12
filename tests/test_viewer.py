import pytest
from src.viewer import display_summary
from unittest.mock import patch
from io import StringIO

def test_display_summary_success():
    # Mock the DBManager to return a summary
    with patch('src.viewer.DBManager') as MockDBManager:
        mock_db_instance = MockDBManager.return_value
        mock_db_instance.get_summary.return_value = {
            'title': 'Test Video Title',
            'url': 'https://youtube.com/watch?v=abc123',
            'date': '2024-01-01',
            'duration': 300,
            'channel_name': 'Test Channel',
            'summary': 'This is a test summary.'
        }

        # Capture stdout
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            display_summary('https://youtube.com/watch?v=abc123')

            result = stdout.getvalue()
            assert "Title: Test Video Title" in result
            assert "URL: https://youtube.com/watch?v=abc123" in result
            assert "Date: 2024-01-01" in result
            assert "Duration: 300 seconds" in result
            assert "Channel: Test Channel" in result
            assert "Summary: This is a test summary." in result

def test_display_summary_not_found():
    # Mock the DBManager to return None (no summary found)
    with patch('src.viewer.DBManager') as MockDBManager:
        mock_db_instance = MockDBManager.return_value
        mock_db_instance.get_summary.return_value = None

        # Capture stdout
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            display_summary('https://youtube.com/watch?v=abc123')
            result = stdout.getvalue()
            assert "No summary found for this video." in result
