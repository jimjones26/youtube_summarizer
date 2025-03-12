import pytest
from src.db_manager import DBManager
from src.viewer import view_summary  # Will cause ImportError initially

def test_view_summary_retrieves_and_formats_data(tmp_path):
    # Setup test environment with temporary DB
    db_path = tmp_path / "test_summaries.db"
    manager = DBManager(db_path)
    manager.create_table()
    
    # Create properly structured test data matching DB schema
    test_url = "https://youtube.com/watch?v=abc123"
    test_metadata = {
        'title': 'Test Video Title',
        'url': test_url,
        'date': '2024-01-01',
        'duration': 300,
        'channel_name': 'Test Channel'
    }
    test_summary = "This is a test summary."
    
    # Store using production code pattern
    manager.store_summary(test_summary, test_metadata)
    manager.close_connection()

    # Attempt to retrieve via viewer component
    result = view_summary(test_url, str(db_path))  # Should error
    
    # Verify full data representation
    assert test_summary in result
    assert test_metadata['title'] in result
    assert test_metadata['url'] in result
    assert test_metadata['date'] in result
    assert str(test_metadata['duration']) in result
    assert test_metadata['channel_name'] in result
