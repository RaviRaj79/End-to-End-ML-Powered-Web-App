from datetime import datetime
from pydantic import BaseModel, Field

class MatchRequest(BaseModel):
    candidate_name: str = Field(default="Anonymous", max_length=100)
    resume_text: str = Field(min_length=20, max_length=20000)
    job_title: str = Field(min_length=2, max_length=160)
    job_description: str = Field(min_length=20, max_length=20000)

class MatchResponse(BaseModel):
    id: int
    score: int
    fit_level: str
    matched_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]

class HistoryItem(BaseModel):
    id: int
    candidate_name: str
    job_title: str
    score: int
    created_at: datetime
