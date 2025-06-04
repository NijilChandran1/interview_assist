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


## Usage

- Start the backend as above.
- Connect a WebSocket client to `ws://localhost:8000/ws/transcribe` and stream audio bytes.
- Use the `/generate-followup` endpoint to get follow-up questions.

## Health Check

Test the backend is running:
curl http://localhost:8000/health


## Notes

- For the full system, use the provided React frontend in the `/frontend` directory.
- Restrict CORS and secure your API keys in production.


# Interview Assistant Frontend

## Setup

1. Install dependencies:
    ```
    npm install
    ```

2. Start the development server:
    ```
    npm start
    ```

The app will connect to the backend at `localhost:8000` by default.

