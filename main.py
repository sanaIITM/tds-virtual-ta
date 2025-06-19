from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from embed_and_search import load_documents, search
import os
import requests

# ✅ Correct AI Proxy endpoint
AI_PROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AI_PROXY_API_KEY = os.environ.get("AI_PROXY_API_KEY")  # must be set in Colab before running

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request format
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # image handling not implemented yet

# ✅ Load course documents once
load_documents("data/all_documents.json")
print("✅ Testing document load...")
test_results = search("GA5 Q8")
print("✅ Found", len(test_results), "matches")
for match in test_results[:2]:
    print(match["text"][:80], "->", match["url"])

# ✅ Health check route
@app.get("/api")
@app.get("/api/")
def health_check():
    return {"status": "ok", "message": "API is running"}

# ✅ Main answer generation endpoint
@app.post("/api")
@app.post("/api/")
async def respond_to_question(req: QuestionRequest):
    query = req.question

    if req.image:
        print("⚠️ Image received but OCR not implemented yet — skipping.")

    # 🔍 Search top relevant snippets
    results = search(query)
    if not results:
        return {
            "answer": "Sorry, I couldn't find a relevant answer.",
            "links": []
        }

    # ✂️ Use top 5 results as context
    context = "\n\n".join([r["text"] for r in results[:5]])

    # 🧠 Prompt messages for the model
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant for IITM's TDS course. Use the context below to answer the question accurately and concisely. Include relevant discussion links."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }
    ]

    # 🔐 AI Proxy headers
    headers = {
        "Authorization": f"Bearer {AI_PROXY_API_KEY}",
        "Content-Type": "application/json"
    }

    # 📤 Request payload
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(AI_PROXY_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
    except Exception as e:
        answer = f"❌ AI Proxy call failed: {str(e)}"

    # 🔗 Format top 3 links
    links = [
        {"url": r["url"], "text": r.get("snippet", r["text"][:100])}
        for r in results[:3]
    ]

    return {
        "answer": answer,
        "links": links
    }



'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from embed_and_search import load_documents, search

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/api")
@app.get("/api/")
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.post("/api")
@app.post("/api/")
async def respond_to_question(req: QuestionRequest):
    query = req.question

    if req.image:
        print("⚠️ Image received but OCR is disabled — skipping.")

    results = search(req.question)
    answer = results[0]["text"] if results else "Sorry, I couldn't find an answer."
    links = [{"url": r["url"], "text": r["snippet"]} for r in results]
    return {"answer": answer, "links": links}

'''
