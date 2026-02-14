from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from app.db.database import Base


class PatientCase(Base):
    __tablename__ = "patient_cases"

    id = Column(Integer, primary_key=True, index=True)

    symptoms = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)

    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    urgency = Column(String, nullable=False)
    reasoning = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
