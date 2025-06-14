import requests
import json
from bs4 import BeautifulSoup

COOKIES = {
    "_t": "KmJoUsKLoUo3L9lATxwJQLxF6%2BymJG1pLzdvhb8NQiih3uweM0wAK3eK6BbsI2B1vBT8LDgfpk7loli4ZcTD87hDQPn0TcVrbE1Bmk9EpVtAPGUgmlh5AwGmJYIpUDcqOjAiqMRKFzaApCeM794A%2F%2BFb6BovfrPT8xm5G9yq56gfGRLFZRuaHa%2F3U8LLyOxCGSeb9HKGQvizYSMd2URRuG0CndK0%2FT6LkyeP9NVlGi3oaUgVmrePmLaa5FW8j366bUbrSRKdmFvb5VGVNNyx2qWRg%2B9%2BjGLhyzCQznTHOg7eyHfSvAZA1CejxCETYPn7--eqUfPlfGXjUGOXwC--h%2F7Tb44JsNxcsoQVUv6%2Few%3D%3D"
# replace with your cookie value
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

def fetch_tds_posts(max_pages=5):
    print("🔄 Scraping TDS Discourse posts...")
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)

    results = []

    for page in range(0, max_pages):
        url = f"{BASE_URL}/c/courses/tds-kb/34.json?page={page}"
        resp = session.get(url)
        data = resp.json()

        for topic in data["topic_list"]["topics"]:
            topic_id = topic["id"]
            slug = topic["slug"]
            topic_url = f"{BASE_URL}/t/{slug}/{topic_id}.json"

            topic_resp = session.get(topic_url)
            topic_data = topic_resp.json()

            first_post = topic_data["post_stream"]["posts"][0]
            cooked_html = first_post["cooked"]
            soup = BeautifulSoup(cooked_html, "html.parser")
            for tag in soup(["img", "a", "code", "pre"]):
               tag.decompose()
            text = soup.get_text(separator=" ").strip()

            results.append({
                "text": text,
                "url": f"{BASE_URL}/t/{slug}/{topic_id}"
            })

        print(f"✅ Page {page} done")

    with open("data/documents.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Saved {len(results)} posts to data/documents.json")

if __name__ == "__main__":
    fetch_tds_posts()

