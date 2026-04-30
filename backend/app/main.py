from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, jobs

app = FastAPI(
    title="eDNA AI Platform API",
    description="API for uploading sequences and managing ML inference jobs",
    version="1.0.0"
)

# CORS config for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1/upload", tags=["upload"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
