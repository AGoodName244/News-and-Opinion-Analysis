from newspaper import Article
from typing import Optional, Dict

def extract_article_text(url: str) -> Optional[Dict[str, str]]:
    """

    :param url:
    :return: {"title": title, "text": text} or None
    """
    try:
        article = Article(url)
        article.download()
        article.parse()

        if not article.text.strip():
            raise ValueError("Empty text")

        return {
            "title": article.title,
            "text": article.text,
        }
    except Exception as e:
        print(f"[Parser Error] {url}: {e}")
        return None