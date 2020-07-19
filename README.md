# SpotifyLibToPlay
Transfers all you music in you library to a playlist for you to be able to share and update existing copies.

## Set up ##
1. Get spotify client_id and client_secret from the spotify developer dashboard by making aa new project.
2. Enter spotify client_id and client_secret inside the `''` in keys.py
3. Enter the uri `http://localhost:5000/actions` to the whitelisted redirect uris in the spotify developer dashboard
4. Create and activate a virtual environment, and install libraries by running
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Run ##
1. Run flask app with `python app.py`
2. Connect on a browser at `http://localhost:5000/`

## To Do ##
* Make purty
* Separate into helper functions
* Authentication Timeout handling
