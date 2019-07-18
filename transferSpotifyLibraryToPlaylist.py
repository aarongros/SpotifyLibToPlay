import requests
import json
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ',
}

data = '{"name":"Library Copy","description":"Copy of the songs in your library","public":false}'

def replaceColon(input):
    output = ''
    for character in input:
        if character == ':':
            output += '%3A'
        else:
            output += character
    return output

def transferMusic():
    # Create Playlist and get id
    response = requests.post('https://api.spotify.com/v1/me/playlists', headers=headers, data=data)
    playlists_id = response.json()['id']
    # Get number of songs
    response = requests.get('https://api.spotify.com/v1/me/tracks?limit=1&offset=0', headers=headers)
    num_requests = float(response.json()["total"]) / 50
    # Add songs
    for i in range(0, int(num_requests)+1):
        print(i)
        response = requests.get('https://api.spotify.com/v1/me/tracks?limit=50&offset=' + str(50*i), headers=headers)
        response = response.json()
        uri = []
        for i in range(0,len(response["items"])):
            uri.append(response["items"][i]["track"]["uri"])
        upload_response = requests.post('https://api.spotify.com/v1/playlists/' + playlists_id + '/tracks', headers=headers, data=json.dumps({'uris': uri}))
