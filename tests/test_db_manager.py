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
