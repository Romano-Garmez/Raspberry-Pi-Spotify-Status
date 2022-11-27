"""
CS50 Final Project: Spotify Status - Roman Garms

Prerequisites

    pip3 install spotipy Flask Flask-Session

    // from your [app settings](https://developer.spotify.com/dashboard/applications)
    export SPOTIPY_CLIENT_ID=client_id_here
    export SPOTIPY_CLIENT_SECRET=client_secret_here
    export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080' // must contain a port
    // SPOTIPY_REDIRECT_URI must be added to your [app settings](https://developer.spotify.com/dashboard/applications)
    // on Windows, use `SET` instead of `export`

Run app.py
    python3 app.py OR python3 -m flask run
"""
import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import json
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)
maxTitleLength = 35
maxArtistLength = 35
maxAlbumLength = 35


@app.route('/')
def index():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-modify-playback-state user-library-read user-library-modify playlist-modify-private playlist-modify-public',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template("login.html", auth_url=auth_url)

    # Step 3. Signed in, display currently playing
    return redirect('/currently_playing')


@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')

@app.route('/currently_playing')
def currently_playing():
    spotify = getSpotify()
    track = spotify.current_user_playing_track()
    if not track is None:
        title = track["item"]["name"]
        artist = get_artists(track["item"]["artists"])
        album = track["item"]["album"]["name"]
        if len(title) > maxTitleLength:
            title = shortenText(title, maxTitleLength)
        if len(artist) > maxArtistLength:
            artist = shortenText(artist, maxArtistLength)
        if len(album) > maxAlbumLength:
            album = shortenText(album, maxAlbumLength)
        art_url = track["item"]["album"]["images"][0]["url"]
        id = track["item"]["id"]
        liked = spotify.current_user_saved_tracks_contains(tracks=[id])[0]
        currently_playing = track["is_playing"]
        return render_template("currently_playing.html", title=title, artist=artist, album=album, art_url=art_url, id=id, currently_playing=currently_playing, liked=liked, json=json.dumps(track, indent=2))
    return render_template("not_playing.html")

#pinged every ~2 sec to see if refresh of page is required
@app.route('/current_track_xhr')
def current_track_xhr():
    spotify = getSpotify()
    track = spotify.current_user_playing_track()
    if not track is None:
        new_id = track["item"]["id"]
        id = request.args.get("id")
        new_currently_playing = track["is_playing"]
        currently_playing = request.args.get("currently_playing") == 'True'
        if id == new_id and currently_playing == new_currently_playing:
            return "same"
        else:
            return "different"
    new_currently_playing = False
    currently_playing = request.args.get("currently_playing") == 'True'
    if currently_playing == new_currently_playing:
        return "same"
    else:
        return "different"

#end of html pages, now just assorted methods

def get_artists(artists_json):
    artists = []
    for artist in artists_json:
        artists.append(artist["name"])
    return ", ".join(artists)

@app.route('/play')
def play():
    spotify = getSpotify()
    spotify.start_playback()
    return redirect('/currently_playing')

@app.route('/pause')
def pause():
    spotify = getSpotify()
    spotify.pause_playback()
    return redirect('/currently_playing')

@app.route('/skip')
def skip():
    spotify = getSpotify()
    spotify.next_track()
    return redirect('/currently_playing')

@app.route('/like')
def like():
    spotify = getSpotify()
    id = request.args.get("id")
    spotify.current_user_saved_tracks_add(tracks=[id])
    return redirect('/currently_playing')

@app.route('/unlike')
def unlike():
    spotify = getSpotify()
    id = request.args.get("id")
    spotify.current_user_saved_tracks_delete(tracks=[id])
    return redirect('/currently_playing')

def getSpotify():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    return spotipy.Spotify(auth_manager=auth_manager)

def shortenText(string, length):
    return string[:length] + "..."

'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
'''
if __name__ == '__main__':
    if os.getenv('SPOTIPY_CLIENT_ID') == None:
        sys.exit("Missing Environment Variable: SPOTIPY_CLIENT_ID")
    if os.getenv('SPOTIPY_CLIENT_SECRET') == None:
        sys.exit("Missing Environment Variable: SPOTIPY_CLIENT_SECRET")
    if os.getenv('SPOTIPY_REDIRECT_URI') == None:
        sys.exit("Missing Environment Variable: SPOTIPY_REDIRECT_URI")
    print(os.getenv("SPOTIPY_REDIRECT_URI"))
    from waitress import serve
    serve(app, host="0.0.0.0", port=8100)
