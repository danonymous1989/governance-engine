from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from weasyprint import HTML
import uuid
import os

app = FastAPI()

class RiskInput(BaseModel):
    context: str

def calculate_score(context: str):
    score = 0
    context = context.lower()

    if "complaint" in context:
        score += 15
    if "ignored" in context or "delay" in context:
        score += 10
    if "acnc" in context or "ndis" in context:
        score += 15
    if "harm" in context:
        score += 20

    return min(score, 100)

def exposure_level(score):
    if score < 35:
        return "Low"
    elif score < 70:
        return "Moderate"
    else:
        return "High"

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/analyze-risk")
def analyze_risk(payload: RiskInput):
    score = calculate_score(payload.context)
    level = exposure_level(score)

    return {
        "context": payload.context,
        "structuralFragilityScore": score,
        "exposureLevel": level
    }

@app.post("/generate-report")
def generate_report(payload: RiskInput):
    score = calculate_score(payload.context)
    level = exposure_level(score)

    html_content = f"""
    <h1>Governance Exposure Stress-Test Report</h1>
    <p><strong>Context:</strong> {payload.context}</p>
    <p><strong>Structural Fragility Score:</strong> {score}</p>
    <p><strong>Exposure Level:</strong> {level}</p>
    """

    file_name = f"/tmp/report_{uuid.uuid4()}.pdf"
    HTML(string=html_content).write_pdf(file_name)

    return FileResponse(file_name, media_type="application/pdf", filename="Governance_Report.pdf")
