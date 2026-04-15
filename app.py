from flask import Flask, render_template, request
from scraper import analyze_site

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    data = None

    if request.method == "POST":
        url = request.form.get("url")

        if url:
            # يصلح الرابط تلقائي
            if not url.startswith("http"):
                url = "https://" + url

            data = analyze_site(url)

        else:
            data = {"error": "اكتب رابط صحيح"}

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run()
