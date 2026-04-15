import requests
from bs4 import BeautifulSoup

def analyze_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    # title
    title = soup.title.string if soup.title else "No title"

    # meta description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag else "N/A"

    # headings
    h1 = len(soup.find_all("h1"))
    h2 = len(soup.find_all("h2"))
    h3 = len(soup.find_all("h3"))

    # links
    links = soup.find_all("a")
    internal = 0
    external = 0

    for link in links:
        href = link.get("href")
        if href:
            if url in href:
                internal += 1
            else:
                external += 1

    return {
        "title": title,
        "description": description,
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "internal_links": internal,
        "external_links": external,
        "score": 70
    }
