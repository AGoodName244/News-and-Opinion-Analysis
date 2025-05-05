from app.models import sentiment, keywords, summary

def analyze_text(text: str) -> dict:
    return {
        "sentiment": sentiment.analyze_sentiment(text),
        "keywords": keywords.extract_keywords(text),
        "summary": summary.generate_summary(text)
    }