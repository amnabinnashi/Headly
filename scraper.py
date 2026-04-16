import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def analyze_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except:
        return {"error": "Failed to connect to the website"}

    if res.status_code != 200:
        return {"error": "Website not responding"}

    soup = BeautifulSoup(res.text, "html.parser")

    # ---------------- TITLE ----------------
    title = soup.title.string.strip() if soup.title else "N/A"

    # ---------------- DESCRIPTION ----------------
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else "N/A"

    # ---------------- HEADINGS ----------------
    h1 = len(soup.find_all("h1"))
    h2 = len(soup.find_all("h2"))
    h3 = len(soup.find_all("h3"))

    # ---------------- LINKS ----------------
    links = soup.find_all("a")
    internal = 0
    external = 0

    domain = urlparse(url).netloc

    for link in links:
        href = link.get("href")
        if href:
            if domain in href:
                internal += 1
            elif href.startswith("http"):
                external += 1

    # ---------------- IMAGES ----------------
    images = soup.find_all("img")
    missing_alt = 0

    for img in images:
        if not img.get("alt"):
            missing_alt += 1

    # ---------------- SCORE ----------------
    score = 50

    if title != "N/A":
        score += 10

    if description != "N/A":
        score += 10

    if h1 == 1:
        score += 10
    elif h1 > 1:
        score += 5

    if h2 > 0:
        score += 5

    if internal > 0:
        score += 5

    if external > 0:
        score += 5

    if missing_alt == 0 and len(images) > 0:
        score += 5

    if score > 100:
        score = 100

    # ---------------- SUGGESTIONS ----------------
    suggestions = []

    if title == "N/A":
        suggestions.append("Add a meta title")

    if description == "N/A":
        suggestions.append("Add a meta description")

    if h1 == 0:
        suggestions.append("Add at least one H1 heading")
    elif h1 > 1:
        suggestions.append("Use only one H1 heading")

    if h2 == 0:
        suggestions.append("Add H2 headings")

    if internal == 0:
        suggestions.append("Add internal links")

    if external == 0:
        suggestions.append("Add external links")

    if missing_alt > 0:
        suggestions.append("Some images are missing alt text")

    # ---------------- RETURN ----------------
    return {
        "title": title,
        "description": description,
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "internal_links": internal,
        "external_links": external,
        "images": len(images),
        "missing_alt": missing_alt,
        "score": score,
        "suggestions": suggestions
    }
