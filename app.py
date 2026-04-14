from flask import Flask, render_template, request
from scraper import WebInsightPro

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
    app.run(debug=True)
