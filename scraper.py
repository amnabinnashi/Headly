import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class WebInsightPro:
    def __init__(self, url):
        self.url = url
        self.soup = None

        self.data = {
            "title": "N/A",
            "description": "N/A",
            "headings": {"h1": 0, "h2": 0, "h3": 0},
            "links": {"internal": 0, "external": 0},
            "seo_score": 0,
            "suggestions": []
        }

    # Fetch website
    def fetch_data(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }

            response = requests.get(self.url, headers=headers, timeout=10)

            if response.status_code != 200:
                return f"Failed to load site ({response.status_code})"

            self.soup = BeautifulSoup(response.text, "html.parser")
            return None

        except Exception as e:
            return str(e)

    # Extract title & meta
    def analyze_meta(self):
        if not self.soup:
            return

        title = self.soup.title.string.strip() if self.soup.title else "N/A"
        self.data["title"] = title

        desc_tag = self.soup.find("meta", attrs={"name": "description"})
        if desc_tag and desc_tag.get("content"):
            self.data["description"] = desc_tag["content"]

    # Headings
    def analyze_headings(self):
        if not self.soup:
            return

        self.data["headings"]["h1"] = len(self.soup.find_all("h1"))
        self.data["headings"]["h2"] = len(self.soup.find_all("h2"))
        self.data["headings"]["h3"] = len(self.soup.find_all("h3"))

    # Links
    def analyze_links(self):
        if not self.soup:
            return

        links = self.soup.find_all("a", href=True)
        domain = urlparse(self.url).netloc

        internal = 0
        external = 0

        for link in links:
            href = link["href"]
            full_url = urljoin(self.url, href)

            if domain in urlparse(full_url).netloc:
                internal += 1
            else:
                external += 1

        self.data["links"]["internal"] = internal
        self.data["links"]["external"] = external

    # SEO Score + Suggestions
    def calculate_seo(self):
        score = 0
        suggestions = []

        # Title
        if self.data["title"] != "N/A":
            score += 20
        else:
            suggestions.append("Add a title tag")

        # Description
        if self.data["description"] != "N/A":
            score += 20
        else:
            suggestions.append("Add meta description")

        # H1
        if self.data["headings"]["h1"] > 0:
            score += 20
        else:
            suggestions.append("Add at least one H1")

        # Links
        if self.data["links"]["internal"] > 0:
            score += 20
        else:
            suggestions.append("Add internal links")

        if self.data["links"]["external"] > 0:
            score += 20
        else:
            suggestions.append("Add external links")

        self.data["seo_score"] = score
        self.data["suggestions"] = suggestions

    # Full report
    def full_report(self):
        self.analyze_meta()
        self.analyze_headings()
        self.analyze_links()
        self.calculate_seo()

        return self.data
