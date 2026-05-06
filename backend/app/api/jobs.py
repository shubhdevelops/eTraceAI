from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/{job_id}")
async def get_job_status(job_id: str):
    job_file = f"/tmp/edna_jobs/{job_id}.json"
    
    if os.path.exists(job_file):
        with open(job_file, "r") as f:
            data = json.load(f)
            return {
                "job_id": job_id,
                "status": data.get("status"),
                "result": data.get("result"),
                "error": None
            }
            
    # If file doesn't exist, it's either pending or failed. 
    # Since we use BackgroundTasks, let's assume it's pending if there's no file.
    return {
        "job_id": job_id,
        "status": "PENDING",
        "result": None,
        "error": None
    }
