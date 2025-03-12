# tests/test_db_manager.py
import sqlite3
import pytest
from src.db_manager import DBManager


def test_create_table():
    # Use an in-memory database for testing
    db_manager = DBManager(':memory:')

    # Force the connection to be established
    db_manager._connect()

    # Attempt to create the table
    db_manager.create_table()

    # Check if the table exists using db_manager's cursor and connection
    cursor = db_manager.cursor
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='summaries'")
    table_exists = cursor.fetchone() is not None
    assert table_exists, "The 'summaries' table should exist"

    # Check table schema.  These names must all exist.
    cursor.execute("PRAGMA table_info(summaries)")
    columns = [row[1] for row in cursor.fetchall()]
    expected_columns = ['id', 'title', 'url', 'date', 'duration', 'channel_name', 'summary']
    for col in expected_columns:
        assert col in columns, f"Column '{col}' is missing from the table"

    db_manager.close_connection()


def test_store_summary():
    db_manager = DBManager(':memory:')
    db_manager._connect()
    db_manager.create_table()

    # Test data with all required fields
    test_metadata = {
        'title': 'Test Video Title',
        'url': 'https://youtube.com/watch?v=abc123',
        'date': '2024-01-01',
        'duration': 300,
        'channel_name': 'Test Channel'
    }
    test_summary = "This is a test summary generated for the video."

    # Store test data using the method we're testing
    db_manager.store_summary(test_summary, test_metadata)

    # Verify database contents
    db_manager.cursor.execute("SELECT * FROM summaries")
    result = db_manager.cursor.fetchone()

    # Validate all fields persisted correctly
    assert result is not None, "No record inserted"
    assert result[1] == test_metadata['title']
    assert result[2] == test_metadata['url']
    assert result[3] == test_metadata['date']
    assert result[4] == test_metadata['duration']
    assert result[5] == test_metadata['channel_name']
    assert result[6] == test_summary

    db_manager.close_connection()
