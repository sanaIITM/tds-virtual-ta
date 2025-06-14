import json

def merge_documents():
    with open("data/documents.json") as f:
        discourse = json.load(f)
    with open("data/course_documents.json") as f:
        course = json.load(f)

    combined = discourse + course
    with open("data/all_documents.json", "w") as f:
        json.dump(combined, f, indent=2)

    print(f"✅ Merged {len(discourse)} discourse + {len(course)} course notes → {len(combined)} total entries.")

if __name__ == "__main__":
    merge_documents()

