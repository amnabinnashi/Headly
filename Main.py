import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


class WebInsightPro:
    def __init__(self, url):
        self.url = url
        self.data = []

    def run(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # استخراج العناوين
            for item in soup.find_all(['h1', 'h2', 'h3']):
                text = item.get_text(strip=True)
                if text:
                    self.data.append({
                        "Type": item.name,
                        "Content": text,
                        "Scraped At": time
