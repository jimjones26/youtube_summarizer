import pytest
from src.summarizer import generate_summary

def test_generate_summary_proportional_length(mocker):
    # Mock Gemini API response
    mock_model = mocker.patch('google.generativeai.GenerativeModel')
    mock_response = mocker.Mock()
    mock_response.text = "Sample summary with appropriate length based on 10min duration."
    mock_model.return_value.generate_content.return_value = mock_response

    # Test input parameters
    transcript = "Long sample transcript text from a 10 minute video. " * 20
    duration = 600  # 600 seconds = 10 minutes

    # Call the summary function
    result = generate_summary(transcript, duration)
    
    # Assert the result contains the mock summary text
    assert "Sample summary with appropriate" in result
    
    # Verify prompt construction with duration scaling
    expected_prompt = (
        "Summarize this YouTube video transcript in 2-3 concise sentences. "
        "The video is 10 minutes long.\n\n"
        f"Transcript: {transcript}"
    )
    mock_model.return_value.generate_content.assert_called_once_with(expected_prompt)
