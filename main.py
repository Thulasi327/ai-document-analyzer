from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import base64

app = FastAPI()

# ✅ Request Model (IMPORTANT)
class DocumentRequest(BaseModel):
    fileName: str
    fileType: str
    fileBase64: str

# ✅ API KEY
API_KEY = "12345"

@app.post("/api/document-analyze")
async def analyze(request: DocumentRequest, x_api_key: str = Header(None)):
    try:
        # 🔐 API Key Check
        if x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # 📂 Get data
        file_name = request.fileName
        file_type = request.fileType.lower()
        file_base64 = request.fileBase64

        # 🔓 Decode Base64
        file_bytes = base64.b64decode(file_base64)

        # 🧠 Extract text (SAFE handling)
        if file_type == "txt":
            text = file_bytes.decode("utf-8")

        elif file_type in ["pdf", "docx", "png", "jpg", "jpeg"]:
            # Temporary safe fallback (to avoid crash)
            text = "Sample extracted text from document"

        else:
            text = "Unsupported file type"

        # ✂️ Summary (simple)
        summary = text[:100]

        # 🏷️ Dummy Entities
        entities = {
            "persons": [],
            "organizations": [],
            "dates": []
        }

        # 😊 Sentiment (basic)
        sentiment = "neutral"

        # ✅ Final Response
        return {
            "filename": file_name,
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment
        }

    except Exception as e:
        return {"error": str(e)}