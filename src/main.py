import argparse
from .extractor import extract_transcript, get_video_metadata
from .summarizer import generate_summary
# Replace: from .db_manager import create_schema, store_summary
from .db_manager import DBManager
from .viewer import display_summary

def main():
    """
    Main function of the YouTube Video Summarizer CLI tool.
    Handles commands to process videos or view saved summaries.
    """
    # Initialize database connection
    db = DBManager("summaries.db")
    db.create_schema()  # Create table schema
    
    # ... rest of existing code ...

    parser = argparse.ArgumentParser(description="YouTube Video Summarizer")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # 'process' command to handle a new video
    process_parser = subparsers.add_parser('process', help='Process a new YouTube video')
    process_parser.add_argument('url', type=str, help='YouTube video URL')

    # 'view' command to display a saved summary
    view_parser = subparsers.add_parser('view', help='View a saved summary')
    view_parser.add_argument('url', type=str, help='YouTube video URL')

    # Parse arguments
    args = parser.parse_args()

    if args.command == 'process':
        # Fetch video metadata
        metadata = get_video_metadata(args.url)
        # Extract transcript
        transcript = extract_transcript(args.url)
        # Generate summary using transcript and duration
        summary = generate_summary(transcript, metadata['duration'])
        # Prepare metadata for storage
        storage_metadata = {
            'title': metadata['title'],
            'url': args.url,
            'date': metadata['upload_date'],
            'duration': metadata['duration'],
            'channel_name': metadata['uploader'],
        }
        # Store using DBManager instance
        db.store_summary(summary, storage_metadata)
        print("Summary generated and stored successfully.")

    elif args.command == 'view':
        # Display the summary for the given URL
        display_summary(args.url)

    else:
        # If no command is provided, show help
        parser.print_help()

    # Close connection at end
    db.close_connection()
