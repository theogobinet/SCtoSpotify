from argparse import ArgumentParser
import core

#Arguments for program execution
parser = ArgumentParser(description='Gets tracks from a SensCritique list and create the corresponding Spotify playlist')

parser.add_argument("-p", "--pid", dest="pid",
                    help="page id of the SensCritique list or top", required=True)
parser.add_argument("-i", "--ignore", 
                    action="store_true", dest="igNF", default=False,
                    help="automatically ignore not found tracks, disable the needs of user input")  
parser.add_argument("-s", "--ignore-sc-uri", 
                    action="store_true", dest="igSC", default=False,
                    help="for top pages, don't try to get the Spotify URI from SensCritique track page, faster but less efficient")                
parser.add_argument("-d", "--disable-check",
                    action="store_true", dest="igCheck", default=False,
                    help="for top pages, disable the Spotify URI verification when URI is obtained through SensCritique, faster but risk of out of date URI")

args = parser.parse_args()

try:
    int(args.pid)
except ValueError:
    print('Wrong page ID')
    exit()

sp, userID = core.spotipy_oath.getSpotifyClient()
soup = core.BeautifulSoup(core.requests.get(f'https://www.senscritique.com/sc2/liste/{args.pid}').text, features="html.parser")

try:
    listName = soup.find('h1', class_='d-heading1 elme-listTitle').text.rstrip()
except AttributeError:
    print ('No list found at the given ID')
    exit()

tracks = core.scGetTracks(sp, args.pid, core.scGetType(soup), soup, not args.igSC, not args.igCheck, args.igNF)

if not tracks:
    print ('No tracks has been found on the given list')
else:
    pl = sp.user_playlist_create(userID, listName, public=False, collaborative=False, description=f'Generated from senscritique.com/sc2/liste/{args.pid} by SCtoSpotify')

    # You can add a maximum of 100 tracks per request
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    for chunk in chunks(tracks, 100):
        sp.user_playlist_add_tracks(userID, pl['id'], chunk, position=None)

    print(f"\nPlaylist '{listName}' created ({len(tracks)} tracks added): {pl['external_urls']['spotify']}")