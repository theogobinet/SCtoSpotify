import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API keys
SPOTIPY_SCOPE = 'playlist-modify-private'
SPOTIPY_CLIENT_ID='client_id'
SPOTIPY_CLIENT_SECRET='client_secret'
SPOTIPY_REDIRECT_URL='http://localhost:8080'

def getSpotifyClient():

    cl = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URL, scope=SPOTIPY_SCOPE))
    return (cl, cl.current_user()['id'])