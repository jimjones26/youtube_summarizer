# tests/test_db_manager.py
import sqlite3
import pytest
from src.db_manager import DBManager  # Import even if it doesn't exist yet


def test_create_table():
    # Use an in-memory database for testing
    db_manager = DBManager(':memory:')

    # Attempt to create the table (it shouldn't exist yet, causing an error if the table creation logic isn't present)
    db_manager.create_table()

    # Now, connect to the in-memory database and check if the table exists
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Check if the table exists by querying the sqlite_master table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='summaries'")
    table_exists = cursor.fetchone() is not None
    assert table_exists, "The 'summaries' table should exist"

    # Check table schema.  These names must all exist.
    cursor.execute("PRAGMA table_info(summaries)")
    columns = [row[1] for row in cursor.fetchall()]
    expected_columns = ['id', 'title', 'url', 'date', 'duration', 'channel_name', 'summary']
    for col in expected_columns:
        assert col in columns, f"Column '{col}' is missing from the table"

    conn.close()
