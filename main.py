from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import uuid

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

    file_name = f"/tmp/report_{uuid.uuid4()}.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, "Governance Exposure Stress-Test Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Context: {payload.context}")
    c.drawString(50, height - 130, f"Structural Fragility Score: {score}")
    c.drawString(50, height - 160, f"Exposure Level: {level}")

    c.save()

    return FileResponse(file_name, media_type="application/pdf", filename="Governance_Report.pdf")rnance_Report.pdf")
