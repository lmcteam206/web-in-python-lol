from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import tldextract
import time
import re

app = FastAPI(title="Website Intelligence API")

# -------------------------
# Helper: Fetch website
# -------------------------
def fetch_site(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        load_time = time.time() - start
        return response, load_time
    except:
        return None, None


# -------------------------
# Metadata Extractor
# -------------------------
@app.get("/metadata")
def metadata(url: str):

    response, load_time = fetch_site(url)

    if not response:
        raise HTTPException(400, "Cannot fetch website")

    soup = BeautifulSoup(response.text, "html.parser")

    def get_meta(name):
        tag = soup.find("meta", attrs={"name": name})
        if tag:
            return tag.get("content")
        return None

    def get_og(property_name):
        tag = soup.find("meta", attrs={"property": property_name})
        if tag:
            return tag.get("content")
        return None

    return {
        "title": soup.title.string if soup.title else None,
        "description": get_meta("description"),
        "keywords": get_meta("keywords"),
        "og_title": get_og("og:title"),
        "og_description": get_og("og:description"),
        "og_image": get_og("og:image"),
        "status_code": response.status_code,
        "load_time": load_time
    }


# -------------------------
# Technology Detector
# -------------------------
@app.get("/technology")
def detect_tech(url: str):

    response, _ = fetch_site(url)

    if not response:
        raise HTTPException(400, "Cannot fetch website")

    html = response.text.lower()

    tech = []

    if "wp-content" in html:
        tech.append("WordPress")

    if "shopify" in html:
        tech.append("Shopify")

    if "react" in html:
        tech.append("React")

    if "next.js" in html:
        tech.append("Next.js")

    if "jquery" in html:
        tech.append("jQuery")

    if "bootstrap" in html:
        tech.append("Bootstrap")

    return {"detected": tech}


# -------------------------
# Link Extractor
# -------------------------
@app.get("/links")
def extract_links(url: str):

    response, _ = fetch_site(url)

    if not response:
        raise HTTPException(400, "Cannot fetch website")

    soup = BeautifulSoup(response.text, "html.parser")

    internal = []
    external = []
    emails = []
    socials = []

    domain = tldextract.extract(url).registered_domain

    for a in soup.find_all("a", href=True):
        link = a["href"]

        if "mailto:" in link:
            emails.append(link.replace("mailto:", ""))

        elif domain in link:
            internal.append(link)

        elif link.startswith("http"):
            external.append(link)

        if any(s in link for s in ["facebook", "twitter", "instagram", "linkedin"]):
            socials.append(link)

    return {
        "internal_links": list(set(internal)),
        "external_links": list(set(external)),
        "emails": list(set(emails)),
        "social_links": list(set(socials))
    }


# -------------------------
# Security Check
# -------------------------
@app.get("/security")
def security_check(url: str):

    response, _ = fetch_site(url)

    if not response:
        raise HTTPException(400, "Cannot fetch website")

    headers = response.headers

    return {
        "https": url.startswith("https"),
        "hsts": "Strict-Transport-Security" in headers,
        "x_frame": "X-Frame-Options" in headers,
        "x_content": "X-Content-Type-Options" in headers
    }
