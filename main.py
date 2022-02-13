from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import CustomSearch, VideoSortOrder


def youtube():
    query: list[dict] = CustomSearch(
        'Hall of Fame by The Script',
        VideoSortOrder.relevance,
        limit=1
    ).result()['result']
    pprint(query)


def spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='a87303d13933408a91e5996bc071209b',
                                                               client_secret='4136795c7e2a45e6a58df44363ced06b'))
    results = sp.search(q='hall of fame', limit=3)
    pprint(results)


if __name__ == '__main__':
    spotify()
