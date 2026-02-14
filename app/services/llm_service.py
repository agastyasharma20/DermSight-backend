
import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)



def generate_clinical_analysis(symptoms, image_data, risk_score, urgency):

    prompt = f"""
You are a responsible dermatology-focused medical triage AI assistant.

Patient symptoms:
{symptoms}

Computed risk score:
{risk_score}

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

Rules:0
If urgency is Emergency due to airway symptoms,
limit differentials to allergic or systemic causes.
Avoid minor dermatologic conditions.

- Do NOT mention cardiac arrest.
- Stay within dermatologic or allergic conditions.
- Do NOT provide definitive diagnosis.
- Keep output medically realistic.
"""


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "summary": content,
            "reasoning": [],
            "differentials": [],
            "warning_signs": []
        }
