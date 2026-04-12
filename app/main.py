from fastapi import FastAPI

app = FastAPI(
    title="IT Asset Intelligence Platform"
)

@app.get("/")
def root():
    return {"message": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}
