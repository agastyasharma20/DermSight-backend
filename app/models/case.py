from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)

    # Core Inputs
    symptoms = Column(Text, nullable=False)

    # Image Analysis
    image_redness_score = Column(Float, nullable=True)

    # Clinical Output
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    urgency = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=True)

    # Explainability
    clinical_reasoning = Column(Text, nullable=True)

    # Follow-up tracking (progress comparison)
    follow_up_of = Column(Integer, ForeignKey("cases.id"), nullable=True)
    parent_case = relationship("Case", remote_side=[id])

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
