import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

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
    return parse_trending(response.text)


def parse_hn(xml: str) -> list[dict]:
    items = []
    for item in ET.fromstring(xml).iterfind("channel/item"):
        items.append(
            {
                "source": "Hacker News",
                "title": item.findtext("title"),
                "url": item.findtext("link"),
                "published_at": parsedate_to_datetime(item.findtext("pubDate")).isoformat(),
                "extra": {"comments": item.findtext("comments")},
            }
        )
    return items


def fetch_hn() -> list[dict]:
    response = httpx.get("https://news.ycombinator.com/rss")
    return parse_hn(response.text)
