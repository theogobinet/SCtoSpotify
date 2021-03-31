`SCtoSpotify` is tool that creates Spotify playlists from Sens Critique lists.

## Table of content

- [Overview](#Overview)
- [Installation](#Installation)
- [Examples](#Authors)
- [License](#License)

## Overview
It is a tool developed in python 3.

Given a Sens Critique list or poll of tracks (won't works for albums, movies, ...), creates the corresponding Spotify playlist using Spotipy librairie.

Spotify API keys are required to use this tool.

Faster for Sens Critique lists (URL like `senscritique.com/liste/xxx/listID`) than polls (URL like `senscritique.com/top/resultats/xxx/listID`), as Spotify URI is directly accessible in lists.

## Installation

Clone the repo and run:

```
    pip install -r requirements.txt 
```

You can put your Spotify API keys in `spotipy_oath.py` so you don't have to enter it in command arguments.

To get Spotify API keys, follow this [guide](https://developer.spotify.com/documentation/web-api/quick-start/) until your app is created.

## Examples

Simple usage, create a Spotify playlist from [this](https://www.senscritique.com/top/resultats/Les_meilleurs_morceaux_de_2016/1212447) Sens Critique poll:
```
python3 SCtoSpotify.py -p 1212447
```
Requires putting your Spotify API keys in `spotipy_oath.py` or you can do:
```
python3 SCtoSpotify.py -p 1212447 -c 'client_id' -e 'client_secret'
```
to avoid it.



## Author
* **Théo GOBINET** - [Elec](https://github.com/theogobinet)
## License
Renamer is licensed under the terms of the MIT Licence 
and is available for free - see the [LICENSE](https://github.com/theogobinet/Renamer/blob/main/LICENSE) file for details.