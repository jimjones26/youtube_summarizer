import argparse
from .extractor import extract_transcript, get_video_metadata
from .summarizer import generate_summary
from .db_manager import create_schema, store_summary
from .viewer import view_summary

def main():
    """
    Main function of the YouTube Video Summarizer CLI tool.
    Handles commands to process videos or view saved summaries.
    """
    # Ensure the database schema is set up
    create_schema()

    # Set up command-line argument parser
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
        # Store summary and metadata in the database
        store_summary(summary, storage_metadata)
        print("Summary generated and stored successfully.")

    elif args.command == 'view':
        # Display the summary for the given URL
        view_summary(args.url)

    else:
        # If no command is provided, show help
        parser.print_help()

if __name__ == "__main__":
    main()