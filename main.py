from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import base64
import os
from utils.pdf_extractor import extract_pdf
from utils.docx_extractor import extract_text_from_docx
from utils.ocr_extractor import extract_image
from utils.nlp_processor import get_summary, get_entities, get_sentiment

app = FastAPI()

# API Key from environment variable
API_KEY = os.getenv("API_KEY", "12345")

class DocumentRequest(BaseModel):
    fileName: str
    fileType: str
    fileBase64: str

@app.post("/api/document-analyze")
async def analyze(request: DocumentRequest, x_api_key: str = Header(None)):
    try:
        # API Key validation
        if x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        file_base64 = request.fileBase64
        file_type = request.fileType.lower()
        file_name = request.fileName
        
        # Decode Base64
        file_bytes = base64.b64decode(file_base64)
        
        # Extract text based on file type
        if file_type == "txt":
            text = file_bytes.decode("utf-8")
        elif file_type == "pdf":
            text = extract_pdf(file_bytes)
        elif file_type == "docx":
            text = extract_text_from_docx(file_bytes)
        elif file_type in ["png", "jpg", "jpeg"]:
            text = extract_image(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Process with NLP
        summary = get_summary(text)
        entities = get_entities(text)
        sentiment = get_sentiment(text)
        
        return {
            "filename": file_name,
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))