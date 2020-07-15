import requests
import json
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}',
}

access_token = 0
all_playlist_ids = []
all_playlist_ids_num_songs = []
all_playlist_names = []

data = '{"name":"Library Copy","description":"Copy of the songs in your library","public":false}'

def replaceColon(input):
    output = ''
    for character in input:
        if character == ':':
            output += '%3A'
        else:
            output += character
    return output

def roundUp(num):
    if num > float(int(num)):
        return int(num) + 1
    return int(num)

def arrayToString(arr):
    string = arr[0]
    for i in range(1, len(arr)):
        string += "%2C" + arr[i]
    return string

def addSongs(playlists_id, uris_to_add):
    # Add all songs
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }
    num_requests = roundUp(float(len(uris_to_add)) / 100)
    for i in range(0, num_requests):
        requests.post('https://api.spotify.com/v1/playlists/' + playlists_id + '/tracks', headers=headers, data=json.dumps({'uris': uris_to_add[i*100:(i+1)*100], "position": i*100}))

def getNumLibraryRequests():
    # Get number of songs and calculate the number of requests needed to get all URIs
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }
    response = requests.get('https://api.spotify.com/v1/me/tracks?limit=1&offset=0', headers=headers)
    response = response.json()
    num_requests = roundUp(float(response["total"]) / 50)
    return num_requests

def getPlaylists():
    # Get existing playlists and prompt to find which to update
    global all_playlist_ids
    global all_playlist_ids_num_songs
    global all_playlist_names
    del all_playlist_ids[:]
    del all_playlist_ids_num_songs[:]
    del all_playlist_names[:]
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    response = response.json()
    for i in range(0,len(response["items"])):
        all_playlist_ids.append(response['items'][i]['id'])
        all_playlist_ids_num_songs.append(int(response['items'][i]['tracks']['total']))
        all_playlist_names.append(response['items'][i]['name'])

def getPlaylistName(playlist_index):
    print(all_playlist_names[playlist_index])

def updatePlaylistCopy(playlist_index):
    # Get playlist id
    playlists_id = all_playlist_ids[playlist_index]
    num_requests = roundUp(float(all_playlist_ids_num_songs[playlist_index]) / 100)

    # Get all songs saved in the playlist
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }
    already_saved_uris = {}
    for i in range(0,num_requests):
        response = requests.get('https://api.spotify.com/v1/playlists/' + playlists_id + '/tracks?limit=100&offset=' + str(100*i), headers=headers)
        response = response.json()
        # Store saved songs in a dictionary
        for j in range(0,len(response["items"])):
            already_saved_uris[response["items"][j]["track"]["uri"]] = 1

    # Get number of library requests needed
    num_requests = getNumLibraryRequests()

    # Get saved songs URIs
    uris_to_add = []
    for i in range(0, num_requests):
        response = requests.get('https://api.spotify.com/v1/me/tracks?limit=50&offset=' + str(50*i), headers=headers)
        response = response.json()
        for j in range(0,len(response["items"])):
            uri = response["items"][j]["track"]["uri"]
            # Check if URIs are already saved
            if uri not in already_saved_uris:
                # If not add them to the playlists
                already_saved_uris[uri] = 1
                uris_to_add.append(uri)

    # Add all songs
    addSongs(playlists_id, uris_to_add)
    return

def createPlaylistCopy(playlist_name):
    # Create Playlist and get id
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }
    data = '{"name":"' + playlist_name + '","description":"Copy of the songs in your library","public":false}'
    response = requests.post('https://api.spotify.com/v1/me/playlists', headers=headers, data=data)
    playlists_id = response.json()['id']

    # Get number of library requests needed
    num_requests = getNumLibraryRequests()

    # Gather the URIs for all the songs
    uris_to_add = []
    for i in range(0, int(num_requests)):
        response = requests.get('https://api.spotify.com/v1/me/tracks?limit=50&offset=' + str(50*i), headers=headers)
        response = response.json()
        for j in range(0,len(response["items"])):
            uris_to_add.append(response["items"][j]["track"]["uri"])

    # Add all songs
    addSongs(playlists_id, uris_to_add)
    return
