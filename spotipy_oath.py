import spotipy
from spotipy.oauth2 import SpotifyPKCE

def getSpotifyClient():
    
    SPOTIPY_CLIENT_ID = 'b31c42d299814284aff107084cbf2816'

    SPOTIPY_SCOPE = 'playlist-modify-private'
    SPOTIPY_REDIRECT_URL = 'http://localhost:8080'

    try:
        cl = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URL, scope=SPOTIPY_SCOPE))
        return (cl, cl.current_user()['id'])

    except spotipy.oauth2.SpotifyOauthError as err:
        print (f"Error with Spotify API connexion: {err}")
