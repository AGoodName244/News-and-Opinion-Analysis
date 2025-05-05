from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text: str, max_length=130, min_length=30):
    words = text.split()
    if len(words) > 512:
        text = " ".join(words[:512])

    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]
