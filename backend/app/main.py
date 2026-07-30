from io import BytesIO
import os
from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import MatchHistory
from .schemas import HistoryItem, MatchRequest, MatchResponse
from .ml import analyze_match

try:
    import multipart  # noqa: F401
    MULTIPART_AVAILABLE = True
except ImportError:
    MULTIPART_AVAILABLE = False

Base.metadata.create_all(bind=engine)
app = FastAPI(title="TalentMatch AI API", version="1.0.0")
cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy"}

if MULTIPART_AVAILABLE:
    @app.post("/api/resume-text")
    async def extract_resume_text(file: UploadFile = File(...)):
        """Extract selectable text from a small PDF resume; no file is persisted."""
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise HTTPException(status_code=503, detail="PDF support is being installed. Run: python -m pip install -r requirements.txt") from exc
        if file.content_type not in {"application/pdf", "application/x-pdf"}:
            raise HTTPException(status_code=415, detail="Please upload a PDF file.")
        content = await file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Please upload a PDF smaller than 5 MB.")
        try:
            reader = PdfReader(BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        except Exception as exc:
            raise HTTPException(status_code=422, detail="This PDF could not be read.") from exc
        if len(text) < 20:
            raise HTTPException(status_code=422, detail="No selectable text was found. Use a text-based PDF or paste your resume.")
        return {"text": text[:20000], "pages": len(reader.pages)}

@app.post("/api/matches", response_model=MatchResponse, status_code=201)
def create_match(payload: MatchRequest, db: Session = Depends(get_db)):
    result = analyze_match(payload.resume_text, payload.job_description)
    record = MatchHistory(candidate_name=payload.candidate_name, resume_text=payload.resume_text, job_title=payload.job_title, job_description=payload.job_description, score=result["score"])
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, **result}

@app.get("/api/matches", response_model=list[HistoryItem])
def list_matches(limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db)):
    return db.query(MatchHistory).order_by(MatchHistory.created_at.desc()).limit(limit).all()

@app.get("/api/matches/{match_id}", response_model=HistoryItem)
def get_match(match_id: int, db: Session = Depends(get_db)):
    record = db.get(MatchHistory, match_id)
    if not record:
        raise HTTPException(status_code=404, detail="Match not found")
    return record
