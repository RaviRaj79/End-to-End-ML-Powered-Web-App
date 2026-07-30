from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class MatchHistory(Base):
    __tablename__ = "match_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_name: Mapped[str] = mapped_column(String(100), default="Anonymous")
    resume_text: Mapped[str] = mapped_column(Text)
    job_title: Mapped[str] = mapped_column(String(160))
    job_description: Mapped[str] = mapped_column(Text)
    score: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
