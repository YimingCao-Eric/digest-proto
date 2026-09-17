from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from digest.sources import fetch_trending

app = FastAPI()


@app.get("/api/items")
def get_items():
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": fetch_trending(),
    }


app.mount("/", StaticFiles(directory="static", html=True))
