import google.generativeai as genai

def generate_summary(transcript: str, duration: int) -> str:
    # Configure API (assumes GOOGLE_API_KEY is set in environment)
    genai.configure()
    
    # Calculate duration-based sentence range
    minutes = duration // 60
    base_sentences = max(2, round(minutes / 5))  # 2 sentences per 5 minutes
    sentence_range = f"{base_sentences}-{base_sentences + 1}"
    
    # Build prompt matching test expectations
    prompt = (
        f"Summarize this YouTube video transcript in {sentence_range} concise sentences. "
        f"The video is {minutes} minutes long.\n\n"
        f"Transcript: {transcript}"
    )
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text
