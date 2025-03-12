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
    try:
        db.create_schema()  # Create table schema
    
        # ... rest of existing code ...

        parser = argparse.ArgumentParser(description="YouTube Video Summarizer")
        # Modify this line
        # parser = argparse.ArgumentParser(description="YouTube Video Summarizer")

        # Add required argument like this:
        # parser.add_argument('command', choices=['process', 'view'], help='Command to execute')
        # parser.add_argument('url', type=str, help='YouTube video URL')
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
            try:
                print(f"Fetching metadata for: {args.url}")
                metadata = get_video_metadata(args.url)
                print(f"Metadata fetched: {metadata['title']}")
                
                print("Extracting transcript...")
                transcript = extract_transcript(args.url)
                
                if not transcript:
                    raise ValueError("Transcript extraction failed")

                print("Generating summary...")
                summary = generate_summary(transcript, metadata['duration'])
                
                storage_metadata = {
                    'title': metadata['title'],
                    'url': args.url,
                    'date': metadata['upload_date'],
                    'duration': metadata['duration'],
                    'channel_name': metadata['uploader'],
                }
                
                db.store_summary(summary, storage_metadata)
                print("Summary stored successfully:\n", summary[:200] + "...")  # Show excerpt
                
            except Exception as e:
                print(f"Error processing video: {str(e)}")

        elif args.command == 'view':
            # Display the summary for the given URL
            display_summary(args.url)

        else:
            # If no command is provided, show help
            parser.print_help()
    finally:
        # Close connection at end
        db.close_connection()
