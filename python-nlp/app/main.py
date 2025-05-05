import atexit

from fastapi import FastAPI
from app.routes import router, executor
from app.redis_worker import start_worker_thread

app = FastAPI(
    title="NLP Analysis Service",
    description="Analyze text to extract sentiment, keywords, and summary",
    version="1.0.0",
)
app.include_router(router)
start_worker_thread()

@atexit.register
def shutdown_executor():
    executor.shutdown()
    print("ThreadPoolExecutor Shutdown finished")