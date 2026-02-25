from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from .database import Base

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    growth_score = Column(Float, nullable=False)
    sustainability_score = Column(Float, nullable=False)
    tension_index = Column(Float, nullable=False)
    zone = Column(String, nullable=False)
    absolem_invoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    