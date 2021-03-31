import interactions
import spotipy_oath
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode 

def searchSpotify(sp, name, rType = 'artist', limit=10):
    names = []
    ids = []

    results = sp.search(q=name,type=rType, limit=limit)
    for result in results[rType + 's']['items']:
        if rType == 'track':
            names.append([result['name'], result['artists'][0]['name']])
        else:
            names.append([result['name']])

        ids.append(result['uri'])
    
    return [names, ids]

def artistTopTracksSpotify(sp, id):
    names = []
    ids = []

    results = sp.artist_top_tracks(id)
    for track in results['tracks']:
        names.append([track['name'], track['artists'][0]['name']])
        ids.append(track['uri'])
    
    return [names, ids]

def urlToID(sp):
    print('Enter a spotify track URL or track ID (leave blank to cancel):')
    while True:
        inp = input('> ')

        if not inp:
            return None

        try:
            return sp.track(inp)['uri']
        except sp.SpotifyException:
            print('Wrong URL or ID, please try again')
        

def selectTrack(sp, trackList, track, artist):
    if not trackList[0]:
        print('No results found')
        return findSpotifyID(sp, track, artist)

    interactions.enumerateMenu([f"'{x[0]}' - '{x[1]}'" for x in trackList[0]]  + ['Not in the listed tracks'])
    selection = interactions.getInt(1, 'track', len(trackList[0]) + 1)

    if selection == len(trackList[0]) + 1:
        return findSpotifyID(sp, track, artist)
    else:
        return trackList[1][selection-1]


def findSpotifyID(sp, track, artist, firstLookup=False, ignoreNF=False):

    if firstLookup:
        initialSearch = searchSpotify(sp, track, 'track')
        for idx, cTr in enumerate(initialSearch[0]):
            if unidecode(cTr[0].lower()) == unidecode(track.lower()) and unidecode(cTr[1].lower()) == unidecode(artist.lower()):
                print(f"\tSame matching track found on Spotify")
                return initialSearch[1][idx]

    if ignoreNF:
        return None

    interactions.clear()
    choices = ['Ignore track', 'Spotify search for track name', 'Spotify search for artist name', 'Enter spotify track URL/ID']
    print (f"\nThe spotify URL for '{track}' of '{artist}' has not be found, what do you want to do ?", )
    interactions.enumerateMenu(choices)
    selection = interactions.getInt(1, 'choice', len(choices))

    if selection == 1:
        return None

    elif selection == 2:
        interactions.clear()
        print(f"List of corresponding tracks for '{track}' of '{artist}':")
        return selectTrack(sp, searchSpotify(sp, track, 'track'), track, artist) 

    elif selection == 3:
        results = searchSpotify(sp, artist)

        if not results[0]:
            print('No results found')
            return findSpotifyID(sp, track, artist)

        interactions.clear()
        print(f"List of corresponding artists for '{artist}':")
        interactions.enumerateMenu([f"'{x[0]}'" for x in results[0]] + ['Not in the listed artists'])
        selection = interactions.getInt(1, 'artist', len(results[0]) + 1)

        if selection == len(results[0]) + 1:
            return findSpotifyID(sp, track, artist, True)
        else:
            artistID = results[1][selection-1]
            interactions.clear()
            print(f"Most popular tracks for '{artist}':")
            return selectTrack(sp, artistTopTracksSpotify(sp, artistID), track, artist)

    elif selection == 4:
        spotId = urlToID(sp)
        if not spotId:
            return findSpotifyID(sp, track, artist)
        
        return spotId

def scUrlToSpotID(sp, url):
    print(f"\tGetting spotify URI from 'https://www.senscritique.com{url}'")
    soup = BeautifulSoup(requests.get(f'https://www.senscritique.com{url}').text, features="html.parser")
    spotID = soup.find('div', class_='d-media-music')

    if spotID:
        # Data from SensCritique can be expired so we need to check that the URI still exist
        try: 
            sp.track(spotID['data-sc-play-value'])
            return spotID['data-sc-play-value']
        except sp.SpotifyException:
            return None
    else:
        return None

def scGetType(soup):
    # Expected: 'Sondages', 'Listes'
    return soup.find_all('a', class_='lahe-breadcrumb-anchor')[-1].text

def scGetTracks(sp, pid, lType, soup, URIfromSC=False, ignoreNF=False):
    tracks = []

    if lType == 'Sondages':

        itemPerPage = len(soup.find_all('li', class_='elpo-item'))
        itemNumbers = 100
        itemType = soup.find('a', class_='elco-anchor')['href'].split('/')[1] 

        if itemType == 'morceau':
                for i in range(1, itemNumbers//itemPerPage + (itemNumbers % itemPerPage > 0) + 1):
                    if i != 1:
                        soup = BeautifulSoup(requests.get(f'https://www.senscritique.com/sc2/top/resultats/{pid}/page-{i}.ajax?limit=1000').text, features="html.parser")

                    for el in soup.find_all('li', class_='elpo-item'):

                        title = el.find('a', class_='elco-anchor').text
                        artist = el.find('a', class_='elco-baseline-a').text

                        print(f"Track: '{title}' of '{artist}':")
                        
                        spotUrl = None

                        if URIfromSC:
                            spotUrl = scUrlToSpotID(sp, el.find('a', class_='elco-anchor')['href'])

                            if not spotUrl:
                                print("\tFailed to get URI for track from SensCritique")

                        if not spotUrl:
                            spotUrl = findSpotifyID(sp, title, artist, True, ignoreNF)

                            if not spotUrl:
                                print(f"\tTrack is ignored and will not be added to the playlist")
                                continue

                        print(f"\tTrack added (uri: {spotUrl})")
                        tracks.append(spotUrl)
        else:
            print('This is not a list of tracks')

    elif lType == 'Listes':

        itemPerPage = 30
        itemInfos = soup.find('div', class_ = "elme-listAuthor")
        itemNumbers = int(itemInfos.find('span').text)
        itemType = itemInfos.find('h2').text.split()[-1]

        if itemType == 'morceaux':

             for i in range(1, itemNumbers//itemPerPage + (itemNumbers % itemPerPage > 0) + 1):
                if i != 1:
                    soup = BeautifulSoup(requests.get(f'https://www.senscritique.com/sc2/liste/{pid}/page-{i}.ajax').text, features="html.parser")

                for el in soup.find_all('li', class_='elli-item'):
                    title = el.find('a', class_='elco-anchor').text.replace("’", "'").replace("Ç","C")
                    artist = el.find('a', class_='elco-baseline-a').text
                    spotUrl = el.find('div', class_='d-media-music')

                    print(f"Track: '{title}' of '{artist}':")

                    if not spotUrl:
                        print("\tFailed to get URI for track from SensCritique")
                        spotUrl = findSpotifyID(sp, title, artist, True, ignoreNF)

                        if not spotUrl:
                            print(f"\tTrack '{title}' is ignored and will not be added to the playlist")
                            continue
                    else:
                        spotUrl = spotUrl['data-sc-play-value']

                    print(f'\tTrack added ({spotUrl})')
                    tracks.append(spotUrl)
        else:
            print('This is not a list of tracks')

    return tracks