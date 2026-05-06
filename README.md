# YouTube Summarizer

A CLI tool that fetches a YouTube video's transcript, generates a concise AI summary scaled to the video's duration, and stores results in a local SQLite database for later retrieval.

## Tech Stack

- **Language:** Python 3
- **AI/LLM:** Google Gemini (`gemini-pro`) via `google-generativeai`
- **Transcript Extraction:** `youtube-transcript-api`
- **Video Metadata:** `youtube-dl`
- **Database:** SQLite (via custom `DBManager` class)
- **CLI:** argparse
- **Testing:** pytest + pytest-mock

## Key Features

- Extracts transcripts from YouTube URLs in standard and short-link formats
- Generates summaries with a duration-aware sentence count (scales with video length)
- Persists summaries to a local SQLite database keyed by video URL
- Retrieves and displays previously saved summaries from the database
- Two CLI commands: `process` (fetch + summarize + store) and `view` (retrieve)

## AI/ML Highlights

Uses Google Gemini (`gemini-pro`) to summarize video transcripts. The prompt is dynamically constructed based on video duration — longer videos receive proportionally more summary sentences. The `GOOGLE_API_KEY` environment variable configures the Gemini client.

## Getting Started

### Prerequisites

- Python 3.8+
- A Google API key with Gemini access

### Installation

```bash
git clone https://github.com/jimjones26/youtube_summarizer.git
cd youtube_summarizer
pip install -r requirements.txt
```

### Environment

```bash
export GOOGLE_API_KEY=your_api_key_here
```

## Usage

```bash
# Process a new video (fetch transcript, generate summary, save to DB)
python -m src process https://www.youtube.com/watch?v=VIDEO_ID

# View a previously saved summary
python -m src view https://www.youtube.com/watch?v=VIDEO_ID
```

### Running Tests

```bash
pytest
```
