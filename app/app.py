from flask import Flask, render_template, request, redirect, url_for
from keys import spotify_client_id, spotify_client_secret
import random
import base64
import requests
import six
import json
import transferSpotifyLibraryToPlaylist as webapi

app = Flask(__name__)

scopes = "playlist-read-collaborative%20playlist-modify-public%20playlist-read-private%20playlist-modify-private%20user-library-read"
state = 123
redirect_uri = "http://127.0.0.1:5000/actions"
refresh_token = ""

@app.route("/")
def home():
    # redirect_uri = url_for('actions')
    print(redirect_uri)
    return render_template("home.html")

@app.route("/login")
def login():
    global state
    state = int(random.random() * 100000)
    url = "https://accounts.spotify.com/authorize?client_id={}&redirect_uri={}&scope={}&response_type=code&state={}".format(spotify_client_id, redirect_uri, scopes, state)
    return redirect(url);

@app.route('/actions')
def actions():
    if state != int(request.args['state']):
        print("Cross-Site Request Forgery Detected")
        return
    if None != request.args.get('error'):
        print("User Denied Access")
        return
    # uri = 'https://accounts.spotify.com/api/token?grant_type=authorization_code&code={}&redirect_uri={}'.format(request.args['code'], redirect_uri)
    # response = requests.post(
    #     uri,
    #     headers={
    #         'Authorization': 'Basic {}'.format(base64.urlsafe_b64encode(six.text_type(spotify_client_id + ":" + spotify_client_secret).encode("ascii")).decode("ascii"))
    #     }
    # )
    payload = {
        "redirect_uri": redirect_uri,
        "code": request.args['code'],
        "grant_type": "authorization_code",
    }
    headers = _make_authorization_headers(spotify_client_id, spotify_client_secret)
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data=payload,
        headers=headers,
        verify=True,
    )
    response = response.json()
    global refresh_token
    webapi.access_token = response["access_token"]
    refresh_token = response["refresh_token"]
    return render_template("actions.html")

def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(
        six.text_type(client_id + ":" + client_secret).encode("ascii")
    )
    return {"Authorization": "Basic %s" % auth_header.decode("ascii")}

@app.route('/get_playlist_name')
def get_playlist_name():
    return render_template("get_playlist_name.html")

@app.route('/list_playlist')
def list_playlist():
    webapi.getPlaylists()
    return render_template("list_playlist.html", playlists = webapi.all_playlist_names)

@app.route('/update_playlist', methods=['POST'])
def update_playlist():
    # webapi.updatePlaylistCopy(int(request.form['playlist']) - 1)
    print(int(request.form['playlist']))
    return render_template("actions.html")


@app.route('/create_new_playlist', methods=['POST'])
def create_new_playlist():
    # webapi.createPlaylistCopy(request.form['playlist_name'])
    print(request.form['playlist_name'])
    return render_template("actions.html")

if __name__ == '__main__':
	app.run(debug=True)
