import requests
import json
import os


crawl_resp = requests.post("http://localhost:8000/api/crawl_and_analyze", json={
    "task_id": "demo_test",
    "keyword": "Tencent",
    "source_url": "https://news.google.com",
    "source_name": "google_news",
    "depth": "shallow"
})

articles = crawl_resp.json()["articles"]
print(f"Got {len(articles)} articles.")

analyzed_results = []
for i, article in enumerate(articles):
    nlp_resp = requests.post("http://localhost:8001/analyze", json={
        "text": article["title"] + article["text"]
    })
    
    result = nlp_resp.json()
    full_result = {
        "url": article["url"],
        "title": article["title"],
        "text": article["text"],
        "summary": result.get("summary"),
        "sentiment": result.get("sentiment"),
        "keywords": result.get("keywords")
    }
    analyzed_results.append(full_result)
os.makedirs("output", exist_ok=True)

with open("output/tiktok_articles.json", "w", encoding="utf-8") as f:
    json.dump(analyzed_results, f, ensure_ascii=False, indent=2)

print("✅ 分析结果已保存到 output/tiktok_articles.json")