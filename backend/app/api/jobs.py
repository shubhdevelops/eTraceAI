from fastapi import APIRouter
from celery.result import AsyncResult
from app.worker.tasks import celery_app

router = APIRouter()

@router.get("/{job_id}")
async def get_job_status(job_id: str):
    res = AsyncResult(job_id, app=celery_app)
    
    # Celery state can be PENDING, STARTED, SUCCESS, FAILURE
    return {
        "job_id": job_id,
        "status": res.state,
        "result": res.result if res.state == 'SUCCESS' else None,
        "error": str(res.result) if res.state == 'FAILURE' else None
    }
