import base64
from io import BytesIO
from PIL import Image
import pytesseract
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from embed_and_search import load_documents, search

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image support (not yet used)

# Load your content
load_documents("data/all_documents.json")
print("✅ Testing document load...")
test_results = search("GA5 Q8")
print("✅ Found", len(test_results), "matches")
for match in test_results:
    print(match["text"][:80], "->", match["url"])

@app.post("/api/")
async def respond_to_question(req: QuestionRequest):
    query = req.question

    # If image is present, try extracting text
    if req.image:
        try:
            image_bytes = base64.b64decode(req.image)
            img = Image.open(BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(img)
            print("🖼️ OCR Extracted:", ocr_text[2080])
            query += "\n\n" + ocr_text
        except Exception as e:
            print("⚠️ Image processing failed:", e)

    results = search(req.question)
    answer = results[0]["text"] if results else "Sorry, I couldn't find an answer."
    links = [{"url": r["url"], "text": r["snippet"]} for r in results]
    return {"answer": answer, "links": links}

