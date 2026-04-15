import requests
from bs4 import BeautifulSoup


class WebInsightPro:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_data(self):
        try:
            res = requests.get(self.url, timeout=10)
            self.soup = BeautifulSoup(res.text, "html.parser")
            return None
        except Exception as e:
            return str(e)

    def get_meta(self):
        title = self.soup.title.string if self.soup.title else "N/A"

        desc_tag = self.soup.find("meta", attrs={"name": "description"})
        desc = desc_tag["content"] if desc_tag else "N/A"

        return title, desc

    def get_headings(self):
        h1 = len(self.soup.find_all("h1"))
        h2 = len(self.soup.find_all("h2"))
        h3 = len(self.soup.find_all("h3"))
        return h1, h2, h3

    def get_links(self):
        links = self.soup.find_all("a", href=True)
        internal = 0
        external = 0

        for link in links:
            if self.url in link["href"]:
                internal += 1
            else:
                external += 1

        return internal, external

    def seo_score(self, h1, desc):
        score = 50
        if h1 > 0:
            score += 20
        if desc != "N/A":
            score += 30
        return min(score, 100)

    def full_report(self):
        title, desc = self.get_meta()
        h1, h2, h3 = self.get_headings()
        internal, external = self.get_links()
        score = self.seo_score(h1, desc)

        suggestions = []
        if h1 == 0:
            suggestions.append("Add H1 heading")
        if desc == "N/A":
            suggestions.append("Add meta description")

        return {
            "score": score,
            "title": title,
            "description": desc,
            "h1": h1,
            "h2": h2,
            "h3": h3,
            "internal": internal,
            "external": external,
            "suggestions": suggestions
        }
