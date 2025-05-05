import time

from newspaper import Article
import requests
from bs4 import BeautifulSoup
import re

def get_google_news_links(keyword, max_links=20):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    query = keyword.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    raw_link = soup.find_all("a", href=True)

    links = []
    for tag in raw_link:
        href = tag["href"]
        match = re.match(r"/url\?q=(https?://[^&]+)&", href)
        if match:
            real_url = match.group(1)
            if real_url not in links:
                links.append(real_url)
            if len(links) >= max_links:
                break
    return links

def extract_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        if not article.text.strip():
            raise ValueError("Empty article.")
        return {
            "url": url,
            "title": article.title,
            "text": article.text,
        }
    except Exception as e:
        print(f"[Error] Failed to process {url} {e}")
        return None

if __name__ == "__main__":
    keyword = "TikTok"
    target_success = 5
    max_links = 20
    print(f"[Info] Start crawling {keyword}")
    urls = get_google_news_links(keyword, max_links)
    results = []
    for url in urls:
        print(f"[Info] Crawling {url}")
        result = extract_article_text(url)
        if result:
            print(f"[Info] Successfully crawled {url}")
            print("Title: ", result["title"])
            print("Preview: ", result["text"][:200], "...\n")
            results.append(result)
        else:
            print("Skipped\n")
        if len(results) >= target_success:
            break
        time.sleep(1)
    print(f"[Info] Finished crawling {keyword}; Got {len(results)} results")