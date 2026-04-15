from flask import Flask, request, jsonify, render_template
from scraper import analyze_site

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze")
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        data = analyze_site(url)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
