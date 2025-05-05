from app.schemas import CrawlTask
from fastapi import HTTPException
from app.crawler.google_new import fetch_articles

def crawl_and_analyze(req: CrawlTask):
    if req.source_name != "google_news":
        raise HTTPException(status_code=400, detail="Unsupported source")

    articles = fetch_articles(req.keyword, req.source_url, req.depth)
    return {
        "task_id": req.task_id,
        "keyword": req.keyword,
        "source": req.source_name,
        "articles_count": len(articles),
        "articles": articles,
    }