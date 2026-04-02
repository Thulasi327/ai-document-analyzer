import spacy
from textblob import TextBlob
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization")

def get_summary(text):
    if len(text) > 1000:
        text = text[:1000]   # avoid model error
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def get_entities(text):
    doc = nlp(text)
    entities = {"persons": [], "organizations": [], "dates": [], "money": []}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["persons"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
        elif ent.label_ == "MONEY":
            entities["money"].append(ent.text)
    return entities

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    return "neutral"