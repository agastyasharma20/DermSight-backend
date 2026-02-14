from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.db.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(Text)
    image_url = Column(String)
    diagnosis = Column(String)
    confidence = Column(Float)
    urgency = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
