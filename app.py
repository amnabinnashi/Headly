from flask import Flask, render_template, request
from Main import WebInsightPro
import os

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


# تشغيل التطبيق (مهم لـ Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
