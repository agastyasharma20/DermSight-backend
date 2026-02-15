
import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)
def generate_clinical_analysis(
    symptoms_text: str,
    redness_score: float,
    confidence: float,
    urgency: str
):
    prompt = f"""
You are a responsible dermatology-focused medical triage AI assistant.

Patient symptoms:
{symptoms_text}

Image redness score:
{redness_score}

Model confidence:
{confidence}

Urgency level:
{urgency}

Respond ONLY in valid JSON format:

{{
  "summary": "2-3 sentence explanation",
  "reasoning": [
    "bullet 1",
    "bullet 2",
    "bullet 3"
  ],
  "differentials": [
    "3 medically reasonable related conditions"
  ],
  "warning_signs": [
    "2-3 realistic escalation symptoms"
  ]
}}

Rules:
If urgency is Emergency due to airway symptoms,
limit differentials to allergic or systemic causes.
Avoid minor dermatologic conditions.
Do NOT provide definitive diagnosis.
Keep output medically realistic.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        return json.loads(content)

    except Exception as e:
        print("LLM ERROR:", e)
        return {
            "summary": "AI explanation temporarily unavailable.",
            "reasoning": [],
            "differentials": [],
            "warning_signs": []
        }
