import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def analyze_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except Exception:
        return {"error": "Failed to connect to the site"}

    if res.status_code != 200:
        return {"error": f"Site returned status code {res.status_code}"}

    soup = BeautifulSoup(res.text, "html.parser")

    score = 0
    suggestions = []

    # ---------------- TITLE ----------------
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    if title:
        score += 20
        if 30 <= len(title) <= 60:
            score += 10
        else:
            suggestions.append("Optimize title length (30–60 characters)")
    else:
        suggestions.append("Add a meta title")

    # ---------------- DESCRIPTION ----------------
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    if description:
        score += 20
        if 50 <= len(description) <= 160:
            score += 10
        else:
            suggestions.append("Optimize description length (50–160 characters)")
    else:
        suggestions.append("Add a meta description")

    # ---------------- HEADINGS ----------------
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")
    h3_tags = soup.find_all("h3")

    h1 = len(h1_tags)
    h2 = len(h2_tags)
    h3 = len(h3_tags)

    if h1 == 1:
        score += 15
    elif h1 > 1:
        score += 5
        suggestions.append("Use only one H1 tag")
    else:
        suggestions.append("Add an H1 tag")

    if h2 > 0:
        score += 10
    else:
        suggestions.append("Add H2 tags for better structure")

    # ---------------- LINKS ----------------
    links = soup.find_all("a", href=True)
    internal = 0
    external = 0

    domain = urlparse(url).netloc

    for link in links:
        href = link.get("href")

        full_url = urljoin(url, href)

        if domain in urlparse(full_url).netloc:
            internal += 1
        else:
            external += 1

    if internal > 0:
        score += 10
    else:
        suggestions.append("Add internal links")

    if external > 0:
        score += 5

    # ---------------- IMAGES ----------------
    images = soup.find_all("img")
    missing_alt = 0

    for img in images:
        if not img.get("alt"):
            missing_alt += 1

    if len(images) > 0:
        if missing_alt == 0:
            score += 10
        else:
            suggestions.append("Some images are missing alt text")
    else:
        suggestions.append("Add images with alt text")

    # ---------------- PAGE SIZE ----------------
    page_size_kb = len(res.content) / 1024

    if page_size_kb < 500:
        score += 5
    else:
        suggestions.append("Reduce page size for better performance")

    # ---------------- FINAL ----------------
    if score > 100:
        score = 100

    return {
        "title": title or "N/A",
        "description": description or "N/A",
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "internal_links": internal,
        "external_links": external,
        "images": len(images),
        "missing_alt": missing_alt,
        "page_size_kb": round(page_size_kb, 2),
        "score": score,
        "suggestions": suggestions
    }
