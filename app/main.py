from fastapi import FastAPI

app = FastAPI(title="Burnout-Proof Decision Engine")

@app.get("/")
def root():
    return {"status": "Deterministic Core Active"}