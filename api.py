import logging

import spotipy
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import CustomSearch, VideoSortOrder

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


def extract_track_info(track: dict) -> dict:
    return {
        'album': {
            'image': track['album']['images'][0]['url'],
            'name': track['album']['name']
        },
        'artists': list(map(lambda artist: artist['name'], track['artists'])),
        'duration_ms': track['duration_ms'],
        'explicit': track['explicit'],
        'name': track['name'],
        'track_number': track['track_number']
    }


@app.get("/search/sp/{query}", status_code=200, response_model=list[dict])
def search_sp(query: str):
    logger.info(f'Handling Spotify request for {query=}')
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id='a87303d13933408a91e5996bc071209b',
            client_secret='4136795c7e2a45e6a58df44363ced06b'
        )
    )

    results = sp.search(q=query, limit=1)['tracks']['items']
    return list(map(extract_track_info, results))


@app.get("/search/yt/{title}", status_code=200)
def search_yt(title: str, artist: str = None):
    search_query = title
    if artist:
        search_query += f' by {artist}'
    logger.info(f'Handling YouTube request for {search_query=}')

    official_video: dict = list(CustomSearch(
        f'{search_query} official',
        VideoSortOrder.relevance,
        limit=1
    ).result()['result'])[0]

    lyrics_video: dict = list(CustomSearch(
        f'{search_query} lyrics',
        VideoSortOrder.relevance,
        limit=1
    ).result()['result'])[0]

    return {
        'official': official_video['link'],
        'lyrics': lyrics_video['link'],
        'title': official_video['title'],

    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8100)
