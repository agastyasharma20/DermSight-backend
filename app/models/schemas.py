from pydantic import BaseModel
from typing import List


class DifferentialDiagnosis(BaseModel):
    condition: str
    confidence: float


class AnalyzeResponse(BaseModel):
    case_id: str
    primary_condition: str
    confidence: float
    urgency_level: str
    reasoning: str
    differential_diagnosis: List[DifferentialDiagnosis]
    recommendations: List[str]
    warning_signs: List[str]
    disclaimer: str
