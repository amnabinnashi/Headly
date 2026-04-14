from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    url = ""

    if request.method == "POST":
        url = request.form.get("url")

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in ["h1", "h2", "h3"]:
                for item in soup.find_all(tag):
                    results.append({
                        "tag": tag.upper(),
                        "text": item.get_text(strip=True)
                    })

        except Exception as e:
            results = [{"tag": "ERROR", "text": str(e)}]

    return render_template("index.html", results=results, url=url)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
