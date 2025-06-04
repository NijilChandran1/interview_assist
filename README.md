# Interview Assistant Backend

This is the backend for a real-time interview assistant using FastAPI, live-transcribe for speech-to-text, and Gemini for LLM-powered follow-up question generation.

## Features

- WebSocket endpoint for real-time audio transcription
- REST endpoint for generating follow-up questions with Gemini
- Logging and exception handling
- Basic tests

## Requirements

- Python 3.9+
- [live-transcribe](https://pypi.org/project/live-transcribe/) (and its dependencies)
- A Google Gemini API key

## Setup

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/interview-assistant.git
    cd interview-assistant/backend
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Set up your `.env` file:
    ```
    GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
    ```

4. Run the backend:
    ```
    uvicorn main:app --reload
    ```

## Testing

Run tests with:
