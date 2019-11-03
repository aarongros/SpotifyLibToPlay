import requests
import json
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQBHeYJsjGbIWmB_OzeygP4-5HkRPnePoBrPsiDzMAqn2gg3TG7wM2wnE5LRLmT__Ns60FTujGOdgNqCNPaWfd_xNnHfaHImSBGn6pnc2e2DG4jCD21597olDzWSq1Hj4hNUBAldoUglqL5_1DLoQm8tqHtVPTt8HQkIt5bJ6b_Dr7uQhI9o-YRaQWME1EWnwF2DG5OjQGq1aE-QA2ZsVykhrlFm6gxZGq---JfJhH5OJchlUndsGOFEXox6QAWFZbo6izLO5rA0qs9XyQ',
}

data = '{"name":"Library Copy TEST","description":"Copy of the songs in your library","public":false}'

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

def updatePlaylistCopy():
    # Get existing playlists
    all_playlist_ids = []
    all_playlist_ids_num_songs = []
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    response = response.json()
    print("Your Playlists")
    for i in range(0,len(response["items"])):
        all_playlist_ids.append(response['items'][i]['id'])
        all_playlist_ids_num_songs.append(int(response['items'][i]['tracks']['total']))
        print(" " + str(i) + " - " + response['items'][i]['name'])
    index = int(input("Enter number of playlist to update: "))
    playlists_id = all_playlist_ids[index]
    num_requests = roundUp(float(all_playlist_ids_num_songs[index]) / 100)

    # Get all songs saved in the playlist
    already_saved_uris = {}
    for i in range(0,num_requests):
        response = requests.get('https://api.spotify.com/v1/playlists/' + playlists_id + '/tracks?limit=100&offset=' + str(100*i), headers=headers)
        response = response.json()
        # Store saved songs in a dictionary
        for j in range(0,len(response["items"])):
            already_saved_uris[response["items"][j]["track"]["uri"]] = 1

    # Get number song requests needed
    response = requests.get('https://api.spotify.com/v1/me/tracks?limit=1&offset=0', headers=headers)
    response = response.json()
    num_requests = roundUp(float(response["total"]) / 50.0)

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
    num_requests = roundUp(float(len(uris_to_add)) / 100)
    for i in range(0, num_requests):
        upload_response = requests.post('https://api.spotify.com/v1/playlists/' + playlists_id + '/tracks', headers=headers, data=json.dumps({'uris': uris_to_add[i*100:(i+1)*100], "position": i*100}))

    return

def createPlaylistCopy():
    # Create Playlist and get id
    response = requests.post('https://api.spotify.com/v1/me/playlists', headers=headers, data=data)
    playlists_id = response.json()['id']

    # Get number of songs and calculate the number of requests needed to get all URIs
    response = requests.get('https://api.spotify.com/v1/me/tracks?limit=1&offset=0', headers=headers)
    response = response.json()
    num_requests = float(response["total"]) / 50
    uris_to_add = []

    # Gather the URIs for all the songs
    for i in range(0, int(num_requests)+1):
        response = requests.get('https://api.spotify.com/v1/me/tracks?limit=50&offset=' + str(50*i), headers=headers)
        response = response.json()
        for j in range(0,len(response["items"])):
            uris_to_add.append(response["items"][j]["track"]["uri"])

    # Add all songs
    num_requests = roundUp(float(len(uris_to_add)) / 100)
    for i in range(0, num_requests):
        upload_response = requests.post('https://api.spotify.com/v1/playlists/' + playlists_id + '/tracks', headers=headers, data=json.dumps({'uris': uris_to_add[i*100:(i+1)*100]}))

    return

updatePlaylistCopy()
