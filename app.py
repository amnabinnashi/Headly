from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        # Meta
        title = soup.title.string if soup.title else "N/A"

        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"] if description_tag else "N/A"

        # Headings
        h1 = len(soup.find_all("h1"))
        h2 = len(soup.find_all("h2"))
        h3 = len(soup.find_all("h3"))

        # Links
        links = soup.find_all("a", href=True)
        internal = 0
        external = 0

        for link in links:
            href = link["href"]
            if href.startswith("http"):
                external += 1
            else:
                internal += 1

        # SEO Score (simple logic)
        score = 50

        if title != "N/A":
            score += 10
        if description != "N/A":
            score += 10
        if h1 > 0:
            score += 10
        if internal > 0:
            score += 10
        if external > 0:
            score += 10

        # Suggestions (English only 🔥)
        suggestions = []

        if title == "N/A":
            suggestions.append("Add a meta title")

        if description == "N/A":
            suggestions.append("Add a meta description")

        if h1 == 0:
            suggestions.append("Add at least one H1 heading")

        if h2 == 0:
            suggestions.append("Add H2 headings")

        if internal == 0:
            suggestions.append("Add internal links")

        if external == 0:
            suggestions.append("Add external links")

        return jsonify({
            "score": score,
            "title": title,
            "description": description,
            "h1": h1,
            "h2": h2,
            "h3": h3,
            "internal_links": internal,
            "external_links": external,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({
            "error": "Failed to analyze site"
        })


if __name__ == "__main__":
    app.run(debug=True)
