import pytest
from src.viewer import view_summary
from src.db_manager import DBManager

def test_view_summary_retrieves_and_formats_data(tmp_path):
    db_path = tmp_path / "test_summaries.db"
    manager = DBManager(db_path)
    
    # REQUIRED CONNECTION STEPS FROM TEST_DB_MANAGER
    manager._connect()  # ESTABLISH CONNECTION
    manager.create_table()
    
    test_metadata = {
        'title': 'Test Video Title',
        'url': 'https://youtube.com/watch?v=abc123',
        'date': '2024-01-01',
        'duration': 300,
        'channel_name': 'Test Channel'
    }
    test_summary = "This is a test summary."
    
    manager.store_summary(test_summary, test_metadata)
    manager.close_connection()  # MAINTAIN CLEAN STATE
    
    result = view_summary(test_metadata['url'], str(db_path))
    
    assert "Title: Test Video Title" in result
    assert "Channel: Test Channel" in result
    assert "Published Date: 2024-01-01" in result
    assert "Summary: This is a test summary." in result

def test_view_summary_handles_missing_summary(tmp_path):
    db_path = tmp_path / "test_summaries.db"
    manager = DBManager(db_path)

    # REQUIRED CONNECTION STEPS FROM TEST_DB_MANAGER
    manager._connect()  # ESTABLISH CONNECTION
    manager.create_table()
    
    test_url = "https://youtube.com/watch?v=missing123"
    
    result = view_summary(test_url, str(db_path))
    
    assert "No summary found for this video." in result
    manager.close_connection()
