from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "/tmp/edna_uploads" # Use S3 in production
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_sequence(file: UploadFile = File(...)):
    if not file.filename.endswith(('.fasta', '.fa', '.txt')):
        raise HTTPException(status_code=400, detail="Only .fasta or .txt files allowed")

    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    from app.worker.tasks import run_inference
    run_inference.apply_async(args=[job_id, file_path], task_id=job_id)
    
    return {"job_id": job_id, "status": "pending", "message": "File uploaded and job queued"}
