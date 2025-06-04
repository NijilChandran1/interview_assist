import React, { useState, useRef } from "react";

function App() {
  const [transcript, setTranscript] = useState([]);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [ws, setWs] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [followup, setFollowup] = useState("");
  const mediaRecorderRef = useRef(null);

  const startTranscription = async () => {
    if (isTranscribing) return;
    setIsTranscribing(true);

    // Open WebSocket connection
    const socket = new window.WebSocket("ws://localhost:8000/ws/transcribe");
    setWs(socket);

    socket.onopen = async () => {
      setSessionId(socket.url.split("/").pop()); // Not robust, demo only

      // Get microphone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new window.MediaRecorder(stream, { mimeType: "audio/webm" });

      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0 && socket.readyState === 1) {
          event.data.arrayBuffer().then((buffer) => {
            socket.send(buffer);
          });
        }
      };

      mediaRecorder.start(250); // 250ms chunks
    };

    socket.onmessage = (event) => {
      setTranscript((prev) => [...prev, event.data]);
    };

    socket.onclose = () => {
      setIsTranscribing(false);
    };
  };

  const stopTranscription = () => {
    setIsTranscribing(false);
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
    if (ws) {
      ws.close();
    }
  };

  const requestFollowup = async () => {
    const resp = await fetch("http://localhost:8000/generate-followup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: ws ? ws.url.split("/").pop() : "" }),
    });
    const data = await resp.json();
    setFollowup(data.question);
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>Live Interview Transcription</h2>
      <button onClick={isTranscribing ? stopTranscription : startTranscription}>
        {isTranscribing ? "Stop" : "Start"} Transcription
      </button>
      <div style={{ margin: "20px 0", minHeight: 100, border: "1px solid #ccc", padding: 10 }}>
        <h4>Live Transcript:</h4>
        {transcript.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </div>
      <button onClick={requestFollowup} disabled={!transcript.length}>
        Generate Follow-Up Question
      </button>
      {followup && (
        <div style={{ marginTop: 20, background: "#f0f0f0", padding: 10 }}>
          <strong>Suggested Follow-Up:</strong>
          <div>{followup}</div>
        </div>
      )}
    </div>
  );
}

export default App;
