import requests
from bs4 import BeautifulSoup
import re

def get_google_news_links(keyword, max_results=5):
    print('Getting Google News Links...')
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    query = keyword.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&tbm=nws"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to get google news links")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    raw_links = soup.find_all('a', href=True)

    # results_blocks = soup.select("div.dbsr")
    links = []
    for tag in raw_links:
        href = tag["href"]
        match = re.match(r"/url\?q=(https?://[^&]+)&", href)
        if match:
            real_url = match.group(1)
            if real_url not in links:
                links.append(real_url)
        if len(links) >= max_results:
            break

    return links
if __name__ == "__main__":
    keyword = "TikTok"
    urls = get_google_news_links(keyword)
    print(f"{len(urls)} links found")
    for url in urls:
        print(url)