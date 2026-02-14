from typing import Dict, List


class TriageEngine:

    def analyze(self, symptoms: str, image_data: Dict, history: Dict = None) -> Dict:

        symptoms_lower = symptoms.lower()
        history = history or {}

        redness = image_data.get("redness_ratio", 0)
        resolution = image_data.get("resolution_quality", "Unknown")

        # ----------------------------
        # 1️⃣ Visual Inflammation Score
        # ----------------------------
        visual_score = min(redness * 2, 1.0)  # Normalize to max 1

        # ----------------------------
        # 2️⃣ Systemic Symptom Score
        # ----------------------------
        systemic_keywords = ["fever", "chills", "fatigue", "body ache"]
        systemic_score = sum(1 for word in systemic_keywords if word in symptoms_lower)
        systemic_score = min(systemic_score * 0.25, 1.0)

        # ----------------------------
        # 3️⃣ Local Severity Score
        # ----------------------------
        local_keywords = ["pain", "swelling", "pus", "warm", "spreading"]
        local_score = sum(1 for word in local_keywords if word in symptoms_lower)
        local_score = min(local_score * 0.25, 1.0)

        # ----------------------------
        # 4️⃣ History Risk Modifier
        # ----------------------------
        history_score = 0

        if history.get("diabetes"):
            history_score += 0.3
        if history.get("immunocompromised"):
            history_score += 0.4
        if history.get("previous_infection"):
            history_score += 0.2

        history_score = min(history_score, 1.0)

        # ----------------------------
        # Final Risk Score
        # ----------------------------
        risk_score = (
            (0.35 * visual_score) +
            (0.30 * systemic_score) +
            (0.20 * local_score) +
            (0.15 * history_score)
        )

        # ----------------------------
        # Triage Classification
        # ----------------------------
        if risk_score < 0.30:
            urgency = "Self Care"
        elif risk_score < 0.55:
            urgency = "Routine"
        elif risk_score < 0.75:
            urgency = "Urgent"
        else:
            urgency = "Emergency"

        # ----------------------------
        # Primary Condition (Basic Mapping)
        # ----------------------------
        if risk_score > 0.65:
            condition = "Possible Skin Infection"
        elif visual_score > 0.4:
            condition = "Inflammatory Dermatitis"
        else:
            condition = "Mild Dermatological Condition"

        return {
            "primary_condition": condition,
            "confidence": round(risk_score, 2),
            "urgency_level": urgency,
            "reasoning": "Risk score derived from multimodal weighted clinical indicators.",
            "clinical_factors": {
                "visual_score": round(visual_score, 2),
                "systemic_score": round(systemic_score, 2),
                "local_score": round(local_score, 2),
                "history_score": round(history_score, 2),
                "final_risk_score": round(risk_score, 2)
            },
            "differential_diagnosis": [],
            "recommendations": self.generate_recommendations(urgency),
            "warning_signs": self.generate_warning_signs(),
            "disclaimer": "This is not a medical diagnosis. Consult a licensed healthcare professional."
        }

    def generate_recommendations(self, urgency: str) -> List[str]:

        if urgency == "Self Care":
            return [
                "Monitor symptoms.",
                "Apply basic skin care.",
                "Seek care if symptoms worsen."
            ]

        if urgency == "Routine":
            return [
                "Schedule outpatient consultation.",
                "Monitor temperature and spread."
            ]

        if urgency == "Urgent":
            return [
                "Seek medical evaluation within 24 hours.",
                "Avoid self-medication.",
                "Monitor for systemic symptoms."
            ]

        return [
            "Seek immediate emergency care.",
            "Go to nearest hospital.",
            "Do not delay treatment."
        ]

    def generate_warning_signs(self) -> List[str]:
        return [
            "Rapid spreading redness",
            "High fever",
            "Severe pain",
            "Difficulty breathing"
        ]
