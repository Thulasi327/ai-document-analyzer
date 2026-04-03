from transformers import pipeline
import spacy
from textblob import TextBlob

# Load once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
nlp = spacy.load("en_core_web_sm")


def get_summary(text):
    if len(text.strip()) == 0:
        return "No content"
    return summarizer(text[:1000], max_length=120, min_length=30, do_sample=False)[0]['summary_text']


def get_entities(text):
    doc = nlp(text)
    return {
        "persons": list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"])),
        "organizations": list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"])),
        "dates": list(set([ent.text for ent in doc.ents if ent.label_ == "DATE"])),
        "money": list(set([ent.text for ent in doc.ents if ent.label_ == "MONEY"]))
    }


def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"