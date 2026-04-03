# Updated extraction and NLP logic

import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_information(text):
    doc = nlp(text)
    # Example extraction logic
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

if __name__ == '__main__':
    sample_text = 'Apple is looking at buying U.K. startup for $1 billion'
    print(extract_information(sample_text))