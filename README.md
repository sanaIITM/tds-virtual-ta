# 📚 TDS Virtual Teaching Assistant

This project implements a FastAPI-based virtual teaching assistant that answers questions using IITM BSc course material (e.g., course notes, discourse discussions). It supports both text queries and returns relevant answers and source links.

---

## 🚀 Features

- Accepts a question via a REST API (`/api/`)
- Retrieves the most relevant answers from course content
- Returns a concise answer and list of relevant links
- Hosted using a static ngrok domain:  
  🌐 [`https://eel-saving-barely.ngrok-free.app/api/`](https://eel-saving-barely.ngrok-free.app/api/)

---

## 📦 Endpoint

### `POST /api/`

#### Request JSON Body

```json
{
  "question": "How does bagging improve decision tree performance?"
}
{
  "answer": "Bagging improves decision tree performance by reducing variance through ensembling...",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/bagging-vs-boosting",
      "text": "Discussion comparing bagging and boosting"
    },
    {
      "url": "https://notes.iitm.ac.in/ml/week6",
      "text": "Notes: Week 6 - Ensemble Methods"
    }
  ]
}
```

🛠 How It Works

     - Loads course content from data/all_documents.json
     - Embeds them using OpenAI embeddings
     - Answers user questions using semantic similarity search
     - Returns the top match with supporting links

📂 Repo Structure
```
tds-virtual-ta/
├── data/
│   └── all_documents.json       # All course content (notes + discourse)
├── embed_and_search.py         # Embedding + search logic
├── main.py                     # FastAPI server and endpoint logic
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```
### ✅ To Run (Colab Friendly)

1. **Install required packages:**

  ```bash
  !pip install fastapi uvicorn nest_asyncio pyngrok
  ```

2. **Clone this repo and start the server using ngrok:**

  ```
  !pip install fastapi uvicorn nest_asyncio pyngrok sentence-transformers --quiet
  
  !git clone https://github.com/sanalITM/tds-virtual-ta.git
  %cd tds-virtual-ta
  
  import nest_asyncio
  from pyngrok import ngrok
  import uvicorn
  
  nest_asyncio.apply()
  ngrok.set_auth_token("replace with ngrok token")
  
  # reserved domain
  public_url = ngrok.connect(addr=8000, domain="eel-saving-barely.ngrok-free.app") #replace with any reserved domain
  print(f"🌐 Public URL: {public_url}")
  
  import main 
  uvicorn.run(main.app, host="0.0.0.0", port=8000)
  ```

3. **Access Swagger UI at:**
 [https://eel-saving-barely.ngrok-free.app/docs]




  This API is meant for the TDS Project - Virtual TA (May 2025).


  
  👤 Author
  
  Sana Bint Salim

