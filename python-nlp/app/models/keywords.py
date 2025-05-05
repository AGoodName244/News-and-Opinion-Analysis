from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text: str, top_k=5) -> list:
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform([text])
    scores = zip(tfidf.get_feature_names_out(), X.toarray()[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_scores[:top_k]]