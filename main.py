from fastapi import FastAPI, File, UploadFile, Header, HTTPException
import shutil
import os

from utils.pdf_extractor import extract_text_pdf
from utils.docx_extractor import extract_text_docx
from utils.ocr_extractor import extract_text_image
from utils.nlp_processor import get_summary, get_entities, get_sentiment

app = FastAPI()

API_KEY = "12345ABCDE"

@app.post("/analyze")
def analyze(file: UploadFile = File(...), x_api_key: str = Header(...)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if file.filename.endswith(".pdf"):
        text = extract_text_pdf(file_location)
    elif file.filename.endswith(".docx"):
        text = extract_text_docx(file_location)
    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_image(file_location)
    else:
        os.remove(file_location)
        raise HTTPException(status_code=400, detail="Unsupported file type")

    os.remove(file_location)

    summary = get_summary(text)
    entities = get_entities(text)
    sentiment = get_sentiment(text)

    return {
        "summary": summary,
        "entities": entities,
        "sentiment": sentiment
    }