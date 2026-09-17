import json
from datetime import datetime, timezone

import feedparser
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
                "body": "",
                "extra": {
                    "language": language.get_text(strip=True) if language else "",
                    "stars_today": int(stars.get_text().split()[0].replace(",", "")),
                    "description": " ".join(description.get_text().split()) if description else "",
                },
            }
        )
    return repos


def stamp_retrieved(items: list[dict]) -> list[dict]:
    today = datetime.now().date().isoformat()
    for item in items:
        item["retrieved_on"] = today
    return items


def fetch_trending() -> list[dict]:
    response = httpx.get("https://github.com/trending?since=daily", follow_redirects=True)
    items = parse_trending(response.text)
    if not items:
        raise ValueError("GitHub Trending: 0 items")
    return stamp_retrieved(items)


def strip_html(markup: str) -> str:
    return " ".join(BeautifulSoup(markup, "html.parser").get_text().split())


def parse_feed(text: str, label: str) -> list[dict]:
    items = []
    for entry in feedparser.parse(text).entries:
        stamp = entry.get("published_parsed") or entry.get("updated_parsed")
        bodies = [block.get("value", "") for block in entry.get("content", [])]
        bodies.append(entry.get("summary", ""))
        items.append(
            {
                "source": label,
                "title": entry.title,
                "url": entry.link,
                "published_at": datetime(*stamp[:6], tzinfo=timezone.utc).isoformat() if stamp else None,
                "body": max((strip_html(body) for body in bodies), key=len),
                "extra": {
                    "authors": [a["name"] for a in entry.get("authors", []) if a.get("name")],
                    "tags": [t["term"] for t in entry.get("tags", []) if t.get("term")],
                },
            }
        )
    items.sort(key=lambda item: (item["published_at"] is not None, item["published_at"] or ""), reverse=True)
    return items


def fetch_feed(url: str, label: str, max_items: int) -> list[dict]:
    response = httpx.get(url, follow_redirects=True)
    items = parse_feed(response.text, label)
    if not items:
        raise ValueError(f"{label}: 0 items")
    return stamp_retrieved(items)[:max_items]


def parse_hf_models(text: str) -> list[dict]:
    models = []
    for entry in json.loads(text):
        models.append(
            {
                "source": "Hugging Face Trending",
                "title": entry["id"],
                "url": "https://huggingface.co/" + entry["id"],
                "published_at": None,
                "body": "",
                "extra": {
                    "likes": entry["likes"],
                    "downloads": entry["downloads"],
                    "trending_score": entry["trendingScore"],
                    "pipeline_tag": entry.get("pipeline_tag", ""),
                    "library_name": entry.get("library_name", ""),
                    "tags": entry["tags"],
                },
            }
        )
    return models


def fetch_hf_models() -> list[dict]:
    response = httpx.get("https://huggingface.co/api/models?sort=trendingScore&limit=20", follow_redirects=True)
    items = parse_hf_models(response.text)
    if not items:
        raise ValueError("Hugging Face Trending: 0 items")
    return stamp_retrieved(items)
