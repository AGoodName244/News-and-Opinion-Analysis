from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Crawler",
    description="Receives keyword + source info from Java, crawls content and return content",
    version="1.0.0",
)

app.include_router(router, prefix="/api", tags=["Crawl Task"])

