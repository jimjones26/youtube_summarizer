import sqlite3

def view_summary(url: str, db_path: str) -> str:
    """Retrieve and format summary from database by URL."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get matching summary with proper SQL injection protection
        cursor.execute('''
            SELECT title, url, date, duration, channel_name, summary 
            FROM summaries 
            WHERE url = ?
        ''', (url,))
        
        result = cursor.fetchone()
        conn.close()

        if not result:
            return "Error: No summary found for this URL"

        # Unpack with schema-matching names
        title, url, date, duration, channel, summary = result
        
        # Create CLI-friendly output format
        return (
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Date: {date}\n"
            f"Duration: {duration} seconds\n"
            f"Channel: {channel}\n\n"
            f"Summary:\n{summary}"
        )

    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
