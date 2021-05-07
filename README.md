`SCtoSpotify` is a tool that creates Spotify playlists from SensCritique lists.

## Table of content

- [Overview](#Overview)
- [Installation](#Installation)
- [Examples](#Authors)
- [License](#License)

## Overview
It is a tool developed in python 3.

Given a Sens Critique list or poll of tracks (won't works for albums, movies, ...), creates the corresponding Spotify playlist using Spotipy librairie.

Faster for Sens Critique lists (URL like `senscritique.com/liste/xxx/listID`) than polls (URL like `senscritique.com/top/resultats/xxx/listID`), as Spotify URI is directly accessible in lists.

## Installation

Clone the repo and run:

```
pip install -r requirements.txt 
```

## Examples

Simple usage, create a Spotify playlist from [this](https://www.senscritique.com/top/resultats/Les_meilleurs_morceaux_de_2016/1212447) Sens Critique poll:
```
python3 SCtoSpotify.py -p 1212447
```

To ignore the non found tracks:
```
python3 SCtoSpotify.py -p 1212447 -i
```
Fastest, but only 80% of tracks found:
```
python3 SCtoSpotify.py -p 1212447 -i -s
```



## Author
* **Théo GOBINET** - [Elec](https://github.com/theogobinet)
## License
SCtoSpotify is licensed under the terms of the MIT Licence 
and is available for free - see the [LICENSE](https://github.com/theogobinet/Renamer/blob/main/LICENSE) file for details.
