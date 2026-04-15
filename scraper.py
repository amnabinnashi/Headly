import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
import pandas as pd

class WebInsightPro:
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.data = []
        self.meta = {}

    def fetch_data(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            self.meta['title'] = soup.title.string if soup.title else "N/A"

            desc = soup.find("meta", attrs={"name": "description"})
            self.meta['description'] = desc['content'] if desc else "N/A"

            tags = ['h1', 'h2', 'h3', 'a']

            for element in soup.find_all(tags):
                content = element.get_text().strip()
                if not content:
                    continue

                entry = {
                    'Type': element.name.upper(),
                    'Content': content,
                    'Link': 'N/A',
                    'Time': datetime.now().strftime("%H:%M:%S")
                }

                if element.name == 'a':
                    href = element.get('href')
                    if href and not href.startswith('#') and not href.startswith('javascript'):
                        entry['Link'] = urljoin(self.url, href)

                self.data.append(entry)

        except Exception as e:
            return str(e)

    def get_dataframe(self):
        return pd.DataFrame(self.data)

    def analyze_structure(self):
        stats = {"H1": 0, "H2": 0, "H3": 0}

        for item in self.data:
            if item['Type'] in stats:
                stats[item['Type']] += 1

        return stats

    def analyze_links(self):
        internal, external = 0, 0
        base_domain = urlparse(self.url).netloc

        for item in self.data:
            link = item['Link']
            if link != "N/A":
                domain = urlparse(link).netloc
                if base_domain in domain:
                    internal += 1
                else:
                    external += 1

        return internal, external

    def seo_score(self, stats):
        score = 100

        if stats['H1'] == 0:
            score -= 30
        if stats['H1'] > 1:
            score -= 20
        if stats['H2'] == 0:
            score -= 10
        if self.meta['description'] == "N/A":
            score -= 20

        return max(score, 0)

    def full_report(self):
        stats = self.analyze_structure()
        internal, external = self.analyze_links()
        score = self.seo_score(stats)

        return {
            "meta": self.meta,
            "stats": stats,
            "internal_links": internal,
            "external_links": external,
            "seo_score": score
        }
