from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    headings = []

    if request.method == "POST":
        url = request.form.get("url")

        # تأكد الرابط فيه http
        if not url.startswith("http"):
            url = "https://" + url

        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            # استخراج H1, H2, H3
            for tag in ["h1", "h2", "h3"]:
                for h in soup.find_all(tag):
                    text = h.get_text(strip=True)
                    if text:
                        headings.append((tag.upper(), text))

        except Exception as e:
            headings.append(("Error", "Failed to fetch website"))

    return render_template("index.html", headings=headings)


# تشغيل السيرفر (مهم لـ Render)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
