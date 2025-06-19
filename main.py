from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from embed_and_search import load_documents, search
import os
import requests

# AI Proxy configuration
AI_PROXY_URL = "https://aiproxy.sanand.workers.dev/v1/chat/completions"
AI_PROXY_API_KEY = os.environ.get("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDA4MjNAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.qkVzh9Uqw0PwaG-Zmi4x0nZ-tCRstVxZgz-gz2r3Ny4")

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

# ✅ Load your content
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

    # Get relevant documents
    results = search(query)
    context = "\n\n".join([r["text"] for r in results[:5]])  # Limit to top 5

    # Prepare system and user messages for AI
    messages = [
        {"role": "system", "content": "You're a helpful assistant for IITM's TDS course. Use the given context to answer the question accurately and link to relevant discussions."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    headers = {
        "Authorization": f"Bearer {AI_PROXY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": messages
    }

    try:
        response = requests.post(AI_PROXY_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
    except Exception as e:
        answer = f"❌ AI Proxy call failed: {str(e)}"

    links = [{"url": r["url"], "text": r["snippet"]} for r in results]
    return {"answer": answer, "links": links}


'''
####
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
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

# ✅ Load course content
load_documents("data/all_documents.json")
print("✅ Testing document load...")
test_results = search("GA5 Q8")
print("✅ Found", len(test_results), "matches")
for match in test_results[:2]:
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
        print("⚠️ Image received but OCR is not enabled — skipping.")

    # 🔍 Search for relevant snippets
    results = search(query)

    if not results:
        return {
            "answer": "Sorry, I couldn't find a relevant answer.",
            "links": []
        }

    # ✅ Generate answer by joining top 2-3 matches
    top_snippets = [r["text"] for r in results[:2]]
    answer = " ".join(top_snippets)

    # 📎 Format links with url + display text (snippet)
    links = [
        {
            "url": r["url"],
            "text": r.get("snippet", r["text"][:100])
        }
        for r in results[:3]
    ]

    return {
        "answer": answer,
        "links": links
    }

'''
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
