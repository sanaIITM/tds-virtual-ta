import os, json
from glob import glob
import markdown
from bs4 import BeautifulSoup

def parse_course_md(md_path):
    with open(md_path, 'r') as f:
        html = markdown.markdown(f.read())
    text = BeautifulSoup(html, 'html.parser').get_text(separator=' ').strip()
    url = md_path
    return {"text": text, "url": url}

def fetch_course_content(folder="tools-in-data-science-public/2025-01"):
    docs = []
    for md in glob(os.path.join(folder, "*.md")):
        docs.append(parse_course_md(md))
    with open("data/course_documents.json", "w") as f:
        json.dump(docs, f, indent=2)
    print(f"✅ Parsed {len(docs)} course docs.")

if __name__ == "__main__":
    fetch_course_content()

