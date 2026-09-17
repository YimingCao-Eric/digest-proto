from datetime import datetime

import httpx
from bs4 import BeautifulSoup


def parse_trending(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    repos = []
    for row in soup.select("article.Box-row"):
        href = row.select_one("h2 a")["href"]
        description = row.select_one("p")
        language = row.select_one('[itemprop="programmingLanguage"]')
        stars = row.select_one("span.float-sm-right")
        repos.append(
            {
                "source": "GitHub Trending",
                "title": href.strip("/"),
                "url": "https://github.com" + href,
                "published_at": None,
                "extra": {
                    "language": language.get_text(strip=True) if language else "",
                    "stars_today": int(stars.get_text().split()[0].replace(",", "")),
                    "description": " ".join(description.get_text().split()) if description else "",
                },
            }
        )
    return repos


def fetch_trending() -> list[dict]:
    response = httpx.get("https://github.com/trending?since=daily")
    items = parse_trending(response.text)
    today = datetime.now().date().isoformat()
    for item in items:
        item["retrieved_on"] = today
    return items
