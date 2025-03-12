from src.db_manager import DBManager

def display_summary(url: str):
    """Retrieves and prints the summary of a YouTube video from the database."""
    db_manager = DBManager()
    summary_data = db_manager.get_summary(url)

    if summary_data:
        print(f"Title: {summary_data['title']}")
        print(f"URL: {summary_data['url']}")
        print(f"Date: {summary_data['date']}")
        print(f"Duration: {summary_data['duration']} seconds")
        print(f"Channel: {summary_data['channel_name']}")
        print(f"Summary: {summary_data['summary']}")
    else:
        print("Error: No summary found for this video.")
