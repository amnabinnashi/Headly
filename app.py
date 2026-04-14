from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def scrape(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    data = []

    # استخراج العناوين
    for tag in ["h1", "h2", "h3"]:
        for h in soup.find_all(tag):
            data.append({
                "type": tag.upper(),
                "text": h.text.strip()
            })

    return data


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        url = request.form.get("url")
        results = scrape(url)

    return render_template("index.html", results=results)


# ✅ هذا الجزء المهم (لازم يكون كذا بالضبط)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
