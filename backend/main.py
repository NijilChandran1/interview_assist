import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import live_transcribe
import google.generativeai as genai
from pydantic import BaseModel

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not set in environment.")
    raise RuntimeError("GOOGLE_API_KEY not set in environment.")

genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONVERSATIONS = {}

@app.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket):
    await websocket.accept()
    buffer = b""
    session_id = id(websocket)
    CONVERSATIONS[session_id] = []
    logger.info(f"WebSocket session {session_id} started.")
    try:
        while True:
            try:
                chunk = await websocket.receive_bytes()
                buffer += chunk
                if len(buffer) > 32000:
                    try:
                        text = live_transcribe.transcribe_bytes(buffer)
                        if text.strip():
                            await websocket.send_text(text)
                            CONVERSATIONS[session_id].append(text)
                        buffer = b""
                    except Exception as e:
                        logger.error(f"Transcription error: {e}")
                        await websocket.send_text("[Transcription error]")
                        buffer = b""
            except Exception as e:
                logger.error(f"WebSocket receive error: {e}")
                break
    except WebSocketDisconnect:
        logger.info(f"WebSocket session {session_id} disconnected.")
    except Exception as e:
        logger.error(f"Unexpected error in WebSocket session {session_id}: {e}")
    finally:
        CONVERSATIONS.pop(session_id, None)
        await websocket.close()

class FollowupRequest(BaseModel):
    session_id: str

@app.post("/generate-followup")
async def generate_followup(req: FollowupRequest):
    try:
        session_id = int(req.session_id)
        conversation = "\n".join(CONVERSATIONS.get(session_id, []))
        if not conversation:
            logger.warning(f"No conversation found for session {session_id}")
            raise HTTPException(status_code=404, detail="Session not found or empty.")
        prompt = (
            "You are an expert technical interviewer. "
            "Given the following interview transcript, suggest an insightful follow-up question for the interviewer to ask the candidate next.\n\n"
            f"Transcript:\n{conversation}\n\nFollow-up question:"
        )
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        logger.info(f"Generated follow-up for session {session_id}")
        return {"question": response.text.strip()}
    except Exception as e:
        logger.error(f"Error generating follow-up: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate follow-up.")

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
