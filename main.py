from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from embed_and_search import load_documents, search
from openai import OpenAI

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image support (OCR skipped for now)

# ✅ Load course and Discourse content
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

    # Optional: Log that image was received (OCR is skipped for now)
    if req.image:
        print("⚠️ Image received but OCR is disabled — skipping.")

    # 🔍 Search documents for relevant context
    results = search(query)
    context = "\n".join([r["snippet"] for r in results[:5]])

    # 💬 Build prompt
    prompt = f"""Answer the student's question based on the following posts from the IITM discourse forum and course content.
If unsure, say you don't know. Provide helpful links when possible.

Question: {query}

Relevant posts:
{context}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the IITM BSc Virtual TA."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"❌ OpenAI API call failed: {str(e)}"

    # 📎 Collect links
    links = [{"url": r["url"], "text": r["snippet"][:100]} for r in results]

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
