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
                "full_name": href.strip("/"),
                "url": "https://github.com" + href,
                "description": " ".join(description.get_text().split()) if description else "",
                "language": language.get_text(strip=True) if language else "",
                "stars_today": int(stars.get_text().split()[0].replace(",", "")),
            }
        )
    return repos


def fetch_trending() -> list[dict]:
    response = httpx.get("https://github.com/trending?since=daily")
    return parse_trending(response.text)
