from flask import Flask, render_template, request
from Main import WebInsightPro

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    data = None

    if request.method == "POST":
        url = request.form.get("url")
        scraper = WebInsightPro(url)
        scraper.run()
        data = scraper.data

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
