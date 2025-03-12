import argparse
import os
from youtube_transcript_api import YouTubeTranscriptApi

def parse_arguments():
    """
    Parse command line arguments for the YouTube summarizer.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description='Summarize YouTube videos using AI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--video-id',
        type=str,
        required=True,
        help='YouTube video ID (e.g., dQw4w9WgXcQ from youtube.com/watch?v=dQw4w9WgXcQ)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='Google API key (can also be set via GOOGLE_API_KEY environment variable)'
    )
    
    return parser.parse_args()

def get_video_transcript(video_id: str) -> tuple[str, int]:
    """
    Get the transcript and duration for a YouTube video.
    
    Args:
        video_id: The YouTube video ID
        
    Returns:
        tuple: (transcript text, video duration in seconds)
    """
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Combine all transcript pieces into one text
    full_transcript = ' '.join([entry['text'] for entry in transcript_list])
    
    # Calculate total duration in seconds
    duration = int(transcript_list[-1]['start'] + transcript_list[-1]['duration'])
    
    return full_transcript, duration

def main():
    """
    Main function of the program.
    Handles command line arguments and orchestrates the summarization process.
    """
    args = parse_arguments()
    
    # Handle API key
    if args.api_key:
        os.environ['GOOGLE_API_KEY'] = args.api_key
    elif 'GOOGLE_API_KEY' not in os.environ:
        print("Error: Google API key not provided. Use --api-key or set GOOGLE_API_KEY environment variable")
        return
    
    try:
        # Get video transcript and duration
        transcript, duration = get_video_transcript(args.video_id)
        
        # TODO: Implement or import the summarization function
        # summary = generate_summary(transcript, duration)
        
        # For now, just print the transcript and duration
        print(f"\nVideo Transcript (Duration: {duration} seconds):")
        print("------------------------------------------")
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
