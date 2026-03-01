from fastapi import FastAPI

app = FastAPI()

# ---------------------------
# SCORING LOGIC
# ---------------------------

def calculate_score(payload):
    score = 0
    context = payload.get("context", "").lower()

    # Complaints escalation risk
    if "complaint" in context:
        score += 15
    if "ignored" in context or "delay" in context:
        score += 10

    # Documentation weakness
    if "verbal" in context or "no record" in context:
        score += 15

    # Oversight failure
    if "board unaware" in context or "not escalated" in context:
        score += 20

    # Regulatory exposure
    if "ndis" in context or "acnc" in context:
        score += 15

    # Stakeholder harm severity
    if "harm" in context or "injury" in context:
        score += 20

    return min(score, 100)


def exposure_level(score):
    if score < 35:
        return "Low"
    elif score < 70:
        return "Moderate"
    else:
        return "High"

# ---------------------------
# ROUTES
# ---------------------------

@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/analyze-risk")
def analyze_risk(payload: dict):

    score = calculate_score(payload)
    level = exposure_level(score)

    return {
        "escalationPathways": "Complaint → Internal handling → Escalation delay → Board visibility risk → Regulatory exposure.",
        "foreseeableHarmIndicators": "Delayed complaint handling, documentation weakness, oversight diffusion.",
        "governanceBlindSpots": "Escalation clarity, board reporting cadence, delegation visibility.",
        "liabilitySignals": "Failure to document decisions, escalation delay risk, potential regulatory notification trigger.",
        "structuralFragilityScore": score,
        "exposureLevel": level,
        "mitigationRecommendations": "Formalise escalation thresholds, implement documented reporting cadence, update risk register."
    }
