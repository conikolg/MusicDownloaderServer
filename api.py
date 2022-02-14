import os
import logging
from typing import List, Dict

import spotipy
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import CustomSearch, VideoSortOrder
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
)


def extract_track_info(track: dict) -> dict:
    return {
        "album": {
            "image": track["album"]["images"][0]["url"],
            "name": track["album"]["name"],
        },
        "artists": list(map(lambda artist: artist["name"], track["artists"])),
        "duration_ms": track["duration_ms"],
        "explicit": track["explicit"],
        "name": track["name"],
        "track_number": track["track_number"],
    }


@app.get("/search/sp/{query}", status_code=200, response_model=List[dict])
def search_sp(query: str, limit: int = 3):
    logger.info(f"Handling Spotify request for {query=}")
    results = sp.search(q=query, limit=limit)["tracks"]["items"]
    return list(map(extract_track_info, results))


class DownloadRequest(BaseModel):
    album: Dict[str, str]
    name: str
    artists: List[str]
    explicit: bool
    track_number: int


@app.put("/download", status_code=200)
def download_track(request: DownloadRequest):
    # Construct YouTube query
    yt_query = f"{request.name} by {request.artists[0]} lyrics"
    logger.info(f"Searching for {yt_query=}")

    # Download song from YouTube
    lyrics_video_link: str = list(
        CustomSearch(f"{yt_query} lyrics", VideoSortOrder.relevance, limit=1).result()[
            "result"
        ]
    )[0]["link"]
    logger.info(f"Downloading video {lyrics_video_link=}")
    # TODO: Start youtube-dl download here

    # TODO: Rename file as needed, apply metadata

    return f"Downloaded video {lyrics_video_link=}"


@app.get("/search/yt/{title}", status_code=200)
def search_yt(title: str, artist: str = None):
    search_query = title
    if artist:
        search_query += f" by {artist}"
    logger.info(f"Handling YouTube request for {search_query=}")

    official_video: dict = list(
        CustomSearch(
            f"{search_query} official", VideoSortOrder.relevance, limit=1
        ).result()["result"]
    )[0]

    lyrics_video: dict = list(
        CustomSearch(
            f"{search_query} lyrics", VideoSortOrder.relevance, limit=1
        ).result()["result"]
    )[0]

    return {
        "official": official_video["link"],
        "lyrics": lyrics_video["link"],
        "title": official_video["title"],
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
