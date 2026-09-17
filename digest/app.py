import tomllib
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from digest.sources import fetch_feed, fetch_hf_models, fetch_trending

app = FastAPI()


def load_sources() -> list[dict]:
    with open("config/sources.toml", "rb") as config:
        return tomllib.load(config)["source"]


@app.get("/api/items")
def get_items():
    fetched_at = datetime.now(timezone.utc).isoformat()
    items = fetch_trending()
    for source in load_sources():
        items += fetch_feed(source["url"], source["label"], source["max_items"])
    items += fetch_hf_models()
    return {
        "fetched_at": fetched_at,
        "items": items,
    }


app.mount("/", StaticFiles(directory="static", html=True))
