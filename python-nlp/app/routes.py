from fastapi import APIRouter, Query
import asyncio
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel

from app.schemas import AnalysisRequest, AnalysisResponse
from app.analyzer import analyze_text as do_analysis
from app.redis_client import push_task, get_task_status
import os

router = APIRouter()
executor = ThreadPoolExecutor()

@router.get("/")
def index():
    return {"message": "NLP Service is running"}

def run_analysis_sync(text: str) -> dict:
    return do_analysis(text)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, run_analysis_sync, request.text)
    return result

class EnqueueRequest(BaseModel):
    task_id: str
    article_id: str
    text: str

class EnqueueResponse(BaseModel):
    message: str
    task: EnqueueRequest
@router.post("/enqueue", response_model=EnqueueResponse)
def enqueue_task(req: EnqueueRequest):
    task = {
        "task_id": req.task_id,
        "article_id": req.article_id,
        "text": req.text,
    }
    push_task(task)
    return {"message": "Task enqueued", "task": task}


@router.get("/status/{task_id}")
def check_task_status(task_id: str, article_ids: list[str] = Query(...)):
    # SAVE_DIR = "output"
    statuses = []
    for aid in article_ids:
        status_info = get_task_status(task_id, aid)
        print(status_info)
        if not status_info:
            status = "unknown"
        else:
            status = status_info.get("status", "pending")
        statuses.append({
            "article_id": aid,
            "status": status
        })

    return {
        "task_id": task_id,
        "status": statuses
    }
    # for aid in article_ids:
    #     filename = f"{task_id}_{aid}.json"
    #     filepath = os.path.join(SAVE_DIR, filename)
    #     if os.path.exists(filepath):
    #         statuses.append({"article_id": aid, "status": "done"})
    #     else:
    #         statuses.append({"article_id": aid, "status": "pending"})
    #
    # return {
    #     "task_id": task_id,
    #     "articles": statuses
    # }