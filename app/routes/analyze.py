from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Optional
from datetime import datetime
import numpy as np
from PIL import Image
import io
import re

from app.db.database import get_db
from app.models.case import Case
from app.services.llm_service import generate_clinical_analysis

router = APIRouter(prefix="/analyze", tags=["Analyze"])


# =====================================================
# CLINICAL RULE ENGINE (Deterministic + Explainable)
# =====================================================

def clinical_risk_engine(symptoms: str, redness_score: float) -> Dict:
    text = symptoms.lower()

    risk_score = 0
    reasoning = []

    # ---------------- TEXT SIGNALS ----------------

    if re.search(r"\bfever\b", text):
        risk_score += 2
        reasoning.append("Fever detected — systemic involvement possible.")

    if re.search(r"\bred\b|\bredness\b", text):
        risk_score += 2
        reasoning.append("Redness reported — inflammatory response suspected.")

    if re.search(r"\bswelling\b", text):
        risk_score += 2
        reasoning.append("Swelling detected — possible allergic reaction.")

    if re.search(r"\bpain\b|\btender\b", text):
        risk_score += 1
        reasoning.append("Pain suggests active inflammatory condition.")

    if re.search(r"\bbreath\b|\bbreathing\b|\bchoking\b", text):
        risk_score += 4
        reasoning.append("Airway involvement suspected — high severity.")

    if re.search(r"\brash\b", text):
        risk_score += 1
        reasoning.append("Rash described — dermatologic involvement likely.")

    # ---------------- IMAGE SIGNAL ----------------

    if redness_score > 60:
        risk_score += 3
        reasoning.append("Severe redness intensity detected in image.")
    elif redness_score > 40:
        risk_score += 2
        reasoning.append("Moderate redness intensity detected in image.")
    elif redness_score > 20:
        risk_score += 1
        reasoning.append("Mild redness detected in image.")

    # ---------------- CLASSIFICATION ----------------

    if risk_score >= 7:
        prediction = "Severe Allergic Reaction or Serious Infection"
        urgency = "Emergency"
        confidence = 0.93

    elif risk_score >= 4:
        prediction = "Possible Skin Infection"
        urgency = "Urgent"
        confidence = 0.86

    elif risk_score >= 2:
        prediction = "Mild Dermatologic Condition"
        urgency = "Monitor"
        confidence = 0.76

    else:
        prediction = "Low Risk Condition"
        urgency = "Routine"
        confidence = 0.66

    urgency_color_map = {
        "Emergency": "RED",
        "Urgent": "ORANGE",
        "Monitor": "YELLOW",
        "Routine": "GREEN"
    }

    return {
        "prediction": prediction,
        "confidence": confidence,
        "urgency": urgency,
        "urgency_color": urgency_color_map[urgency],
        "risk_score": risk_score,
        "clinical_reasoning": reasoning
    }


# =====================================================
# IMAGE PROCESSING
# =====================================================

def calculate_redness(contents: bytes) -> float:
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img_array = np.array(img)

    red = img_array[:, :, 0]
    green = img_array[:, :, 1]
    blue = img_array[:, :, 2]

    redness = np.mean(red - (green + blue) / 2)
    return float(max(0, redness))


# =====================================================
# ANALYZE ENDPOINT
# =====================================================

@router.post("/")
async def analyze_case(
    symptoms: str = Form(...),
    image: UploadFile = File(...),
    follow_up_case_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):

    if len(symptoms.strip()) < 5:
        raise HTTPException(status_code=400, detail="Symptoms too short.")

    if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG allowed.")

    # ---------------- PROCESS IMAGE ----------------
    try:
        contents = await image.read()
        redness_score = calculate_redness(contents)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    # ---------------- CORE TRIAGE ----------------
    result = clinical_risk_engine(symptoms, redness_score)

    # ---------------- EMERGENCY OVERRIDE ----------------
    emergency_action = None
    if result["urgency"] == "Emergency":
        emergency_action = "🚨 SEEK IMMEDIATE MEDICAL CARE. CALL EMERGENCY SERVICES."

    # ---------------- PROGRESS TRACKING ----------------
    improvement = None
    previous_redness = None

    if follow_up_case_id:
        previous_case = db.query(Case).filter(Case.id == follow_up_case_id).first()
        if previous_case:
            previous_redness = previous_case.image_redness_score

            if previous_redness:
                change = previous_redness - redness_score
                improvement = round((change / previous_redness) * 100, 2)

    # ---------------- LLM EXPLANATION ----------------
    try:
        ai_explanation = generate_clinical_analysis(
            symptoms_text=symptoms,
            redness_score=redness_score,
            confidence=result["confidence"],
            urgency=result["urgency"]
        )
    except Exception:
        ai_explanation = {
            "summary": "AI explanation unavailable.",
            "reasoning": [],
            "differentials": [],
            "warning_signs": []
        }

    # ---------------- SAVE CASE ----------------
    new_case = Case(
        symptoms=symptoms,
        prediction=result["prediction"],
        confidence=result["confidence"],
        urgency=result["urgency"],
        image_redness_score=redness_score,
        created_at=datetime.utcnow()
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    # ---------------- FINAL RESPONSE ----------------
    return {
        "case_id": new_case.id,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "urgency": result["urgency"],
        "urgency_color": result["urgency_color"],
        "risk_score": result["risk_score"],
        "clinical_reasoning": result["clinical_reasoning"],
        "image_redness_score": redness_score,
        "improvement_percentage": improvement,
        "emergency_action": emergency_action,
        "ai_explanation": ai_explanation,
        "disclaimer": "This is not a medical diagnosis. Seek professional medical advice."
    }
