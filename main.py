from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/analyze-risk")
def analyze_risk(payload: dict):
    return {
        "escalationPathways": "Example escalation pathway output.",
        "foreseeableHarmIndicators": "Example harm indicators.",
        "governanceBlindSpots": "Example blind spots.",
        "liabilitySignals": "Example liability signals.",
        "structuralFragilityScore": 62.5,
        "exposureLevel": "Moderate",
        "mitigationRecommendations": "Example mitigation steps."
    }
