import os
# A shared in-memory database keeps tests isolated and filesystem-independent.
os.environ["DATABASE_URL"] = "sqlite://"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
PAYLOAD = {"candidate_name":"Ava", "resume_text":"Python React Docker SQL FastAPI developer with API experience.", "job_title":"Full Stack Engineer", "job_description":"Need Python, React, Docker and SQL experience building REST API services."}

def test_health(): assert client.get("/health").json()["status"] == "healthy"
def test_create_match():
    response = client.post("/api/matches", json=PAYLOAD)
    assert response.status_code == 201
    assert response.json()["score"] >= 0
def test_history_lists_records(): assert client.get("/api/matches").status_code == 200
def test_history_rejects_invalid_limit(): assert client.get("/api/matches?limit=0").status_code == 422
def test_resume_upload_route_is_available():
    response = client.post("/api/resume-text", files={"file": ("resume.pdf", b"not a PDF", "application/pdf")})
    assert response.status_code == 422
def test_not_found(): assert client.get("/api/matches/999999").status_code == 404
def test_rejects_short_resume():
    invalid = {**PAYLOAD, "resume_text":"too short"}
    assert client.post("/api/matches", json=invalid).status_code == 422
