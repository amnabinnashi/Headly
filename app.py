from flask import Flask, render_template, request, jsonify
from scraper import WebInsightPro
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    tool = WebInsightPro(url)
    error = tool.fetch_data()

    if error:
        return jsonify({"error": error}), 500

    report = tool.full_report()

    return jsonify(report)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
