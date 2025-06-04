from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_followup_no_session():
    response = client.post("/generate-followup", json={"session_id": "999999"})
    assert response.status_code == 404
