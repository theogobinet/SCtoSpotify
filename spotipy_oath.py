import spotipy
from spotipy.oauth2 import SpotifyOAuth

def getSpotifyClient(client_id = None, client_secret = None):

    # Change this
    SPOTIPY_CLIENT_ID = 'client_id'
    SPOTIPY_CLIENT_SECRET = 'client_secret'

    SPOTIPY_SCOPE = 'playlist-modify-private'
    SPOTIPY_REDIRECT_URL = 'http://localhost:8080'


    if not client_id or not client_secret:
        if SPOTIPY_CLIENT_ID == 'client_id' or SPOTIPY_CLIENT_SECRET == 'client_secret':
            print('Please put your Spotify API keys in spotipy_oath.py or in as command line arguments')
            exit()
    else:
        SPOTIPY_CLIENT_ID = client_id
        SPOTIPY_CLIENT_SECRET = client_secret

    try:
        cl = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URL, scope=SPOTIPY_SCOPE))
        return (cl, cl.current_user()['id'])

    except spotipy.oauth2.SpotifyOauthError as err:
        print (f"Error with Spotify API connexion: {err}")
