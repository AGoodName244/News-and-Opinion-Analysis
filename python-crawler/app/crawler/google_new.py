import requests
from bs4 import BeautifulSoup
import re
import time
from app.extractor.article_parser import extract_article_text
from typing import List, Dict

DEPTH_MAP = {
    "shallow": 5,
    "medium": 20,
    "deep": 50,
}

def get_google_news_links(keyword: str, max_links: int) -> List[str]:
    print("Getting Google News Links...")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    query = keyword.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}&tbm=nws"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    raw_links = soup.find_all("a", href=True)
    links = []
    for tag in raw_links:
        href = tag["href"]
        match = re.match(r"/url\?q=(https?://[^&]+)&", href)
        if match:
            real_url = match.group(1)
            if real_url not in links:
                links.append(real_url)
        if len(links) >= max_links:
            break
    print(len(links))
    return links

def fetch_articles(keyword: str, source_url: str, depth: str) -> List[Dict]:
    print("Fetching articles...")
    target_count = DEPTH_MAP.get(depth)
    max_candidates = 3 * target_count

    links = get_google_news_links(keyword, max_links=max_candidates)

    valid_results = []
    for url in links:
        result = extract_article_text(url)
        if result is None:
            continue
        title, text = result["title"], result["text"]
        if text.lower().count(keyword.lower()) >= 2:
            valid_results.append({
                "url": url,
                "title": title,
                "text": text,
            })
        if len(valid_results) >= target_count:
            break

        time.sleep(1)
    print(len(valid_results))
    return valid_results