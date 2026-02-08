from fastapi import FastAPI, HTTPException, Request, Header
import requests
from bs4 import BeautifulSoup
import tldextract
import time
from urllib.parse import urljoin, urlparse
from collections import defaultdict

app = FastAPI(title="Website Intelligence API")

# ----------------------------
# Configuration
# ----------------------------
API_KEYS = {"YOUR_SECRET_KEY_1", "YOUR_SECRET_KEY_2"}  # Replace with your API keys
REQUEST_LIMIT = 60  # requests
TIME_WINDOW = 60  # seconds

requests_per_ip = defaultdict(list)

# ----------------------------
# Requests Session
# ----------------------------
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})

# ----------------------------
# Helper: Validate URL
# ----------------------------
def validate_url(url: str):
    if not url.startswith("http"):
        url = "https://" + url
    return url

# ----------------------------
# Helper: Fetch Website
# ----------------------------
def fetch_site(url):
    url = validate_url(url)
    try:
        start = time.time()
        response = session.get(url, timeout=8)
        load_time = round(time.time() - start, 3)
        return response, load_time, url
    except requests.exceptions.RequestException:
        return None, None, None

# ----------------------------
# Helper: Verify API Key
# ----------------------------
def verify_api_key(x_api_key: str = Header(...)):
    pass  # do nothing, RapidAPI already handles authentication

# ----------------------------
# Helper: Rate Limiter
# ----------------------------
def rate_limiter(request: Request):
    ip = request.client.host
    now = time.time()
    window_start = now - TIME_WINDOW
    requests_per_ip[ip] = [t for t in requests_per_ip[ip] if t > window_start]
    if len(requests_per_ip[ip]) >= REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests")
    requests_per_ip[ip].append(now)

# ----------------------------
# Health Endpoints
# ----------------------------
@app.get("/", summary="Home", description="Check if API is running")
def home():
    return {"status": "Website Intelligence API running"}

@app.get("/health", summary="Health Check", description="Check if API is running")
def health():
    return {"status": "ok"}

# ----------------------------
# Metadata Endpoint
# ----------------------------
@app.get("/metadata", summary="Get Website Metadata", description="Returns metadata, OpenGraph tags, status code, and load time")
def metadata(url: str, request: Request, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    rate_limiter(request)

    response, load_time, url = fetch_site(url)
    if not response:
        raise HTTPException(400, "Cannot fetch website")

    soup = BeautifulSoup(response.text, "html.parser")

    def get_meta(name):
        tag = soup.find("meta", attrs={"name": name})
        return tag.get("content") if tag else None

    def get_og(prop):
        tag = soup.find("meta", attrs={"property": prop})
        return tag.get("content") if tag else None

    title = soup.title.string.strip() if soup.title else None

    return {
        "url": url,
        "title": title,
        "description": get_meta("description"),
        "keywords": get_meta("keywords"),
        "og_title": get_og("og:title"),
        "og_description": get_og("og:description"),
        "og_image": get_og("og:image"),
        "status_code": response.status_code,
        "load_time": load_time
    }

# ----------------------------
# Technology Detection
# ----------------------------
@app.get("/technology", summary="Detect Website Technology", description="Detects frameworks and CMS used on the website")
def detect_tech(url: str, request: Request, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    rate_limiter(request)

    response, _, url = fetch_site(url)
    if not response:
        raise HTTPException(400, "Cannot fetch website")

    html = response.text.lower()
    tech = []
    checks = {
        "WordPress": "wp-content",
        "Shopify": "shopify",
        "React": "react",
        "Next.js": "next.js",
        "jQuery": "jquery",
        "Bootstrap": "bootstrap"
    }
    for name, keyword in checks.items():
        if keyword in html:
            tech.append(name)

    return {
        "url": url,
        "detected": tech
    }

# ----------------------------
# Link Extractor
# ----------------------------
@app.get("/links", summary="Extract Links", description="Returns internal links, external links, emails, and social media links")
def extract_links(url: str, request: Request, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    rate_limiter(request)

    response, _, url = fetch_site(url)
    if not response:
        raise HTTPException(400, "Cannot fetch website")

    soup = BeautifulSoup(response.text, "html.parser")
    internal = set()
    external = set()
    emails = set()
    socials = set()

    parsed = urlparse(url)
    base_domain = parsed.netloc

    for a in soup.find_all("a", href=True):
        link = urljoin(url, a["href"])

        if link.startswith("mailto:"):
            emails.add(link.replace("mailto:", ""))
        elif base_domain in link:
            internal.add(link)
        elif link.startswith("http"):
            external.add(link)

        if any(s in link for s in ["facebook.com", "twitter.com", "instagram.com", "linkedin.com"]):
            socials.add(link)

    return {
        "url": url,
        "internal_links": list(internal),
        "external_links": list(external),
        "emails": list(emails),
        "social_links": list(socials)
    }

# ----------------------------
# Security Headers
# ----------------------------
@app.get("/security", summary="Check Security Headers", description="Checks HTTPS, HSTS, X-Frame, X-Content-Type, and X-XSS headers")
def security_check(url: str, request: Request, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    rate_limiter(request)

    response, _, url = fetch_site(url)
    if not response:
        raise HTTPException(400, "Cannot fetch website")

    headers = response.headers
    return {
        "url": url,
        "https": url.startswith("https"),
        "hsts": "Strict-Transport-Security" in headers,
        "x_frame": "X-Frame-Options" in headers,
        "x_content": "X-Content-Type-Options" in headers,
        "x_xss": "X-XSS-Protection" in headers
    }
