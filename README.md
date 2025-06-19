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

   Just run the following code in colab : thank me later :)
  ```
# Step 1: Install dependencies
!pip install fastapi uvicorn nest_asyncio pyngrok --quiet

# Step 2: Clone my public GitHub repo
!git clone --depth=1 https://github.com/sanaIITM/tds-virtual-ta.git
%cd tds-virtual-ta

# Step 3: Import and run your FastAPI app
from pyngrok import ngrok
import nest_asyncio
import uvicorn
import main  # this is your main.py

# Step 4: Connect with static domain from ngrok
ngrok.set_auth_token("replace with you ngrok auth token") #get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken
public_url = ngrok.connect(addr=8000, domain="replace with your subdomain ") # under domain (https://dashboard.ngrok.com/domains) select create domain and get your url
print("🌐 Public URL:", public_url)

# Step 5: Run app
nest_asyncio.apply()
uvicorn.run(main.app, host="0.0.0.0", port=8000)

  ```

3. **Access Swagger UI at:**
 [https://eel-saving-barely.ngrok-free.app/docs]




  This API is meant for the TDS Project - Virtual TA (May 2025).


  
  👤 Author
  
  Sana Bint Salim

