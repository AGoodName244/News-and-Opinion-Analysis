import threading
import time
from app.redis_client import pop_task_blocking, set_task_status
from app.analyzer import analyze_text
import json
import os

SAVE_DIR = "output"
os.makedirs(SAVE_DIR, exist_ok=True)

def worker_loop():
    print("[Worker started], waiting for task...")
    while True:
        task = pop_task_blocking(timeout=10)
        if task is None:
            continue
        task_id = task.get("task_id")
        article_id = task.get("article_id")
        text = task.get("text")
        set_task_status(task_id, article_id, "pending")
        print(f"[Worker] is working on task {task_id}, article {article_id}")

        try:
            result = analyze_text(text)
            # result_record = {
            #     "task_id": task_id,
            #     "article_id": article_id,
            #     **result,
            # }

            # path = os.path.join(SAVE_DIR, f"{task_id}_{article_id}.json")
            # with open(path, "w", encoding="utf-8") as f:
            #     json.dump(result_record, f, ensure_ascii=False, indent=4)

            redis_result = {
                "status": "done",
                "summary": result.get("summary", ""),
                "sentiment": result.get("sentiment", ""),
                "keywords": result.get("keywords", ""),
                # "content": text,
            }

            set_task_status(task_id, article_id, extra=redis_result)
            print(f"[Worker] done task {task_id}, article {article_id}")

        except Exception as e:
            set_task_status(task_id, article_id, extra={
                "status": "error",
                "error": str(e)
            })
            print(f"[Worker] failed on task {task_id}, article {article_id}, error: str{e}")

def start_worker_thread():
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()

