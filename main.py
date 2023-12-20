from flask import Flask, render_template, request
from flask_restful import Api, Resource
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import sqlite3
import datetime
import os
import json

load_dotenv()

USERNAME = os.getenv("USERNAME")
SCOPE = os.getenv("SCOPE")
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
HOST = os.getenv("HOST")

token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)

app = Flask(__name__)
api = Api(app)

conn = sqlite3.connect("static\database\song.sqlite", check_same_thread=False)
cursor = conn.cursor()

class serachSong(Resource):
    def get(self, search):
        search = sp.search(q=search, type="track", limit=6)
        json_object = json.dumps(search, indent=4)
 
        # Writing to sample.json
        with open("output.json", "w") as outfile:
            outfile.write(json_object)
        return search
    
class detail(Resource):
    def get(self, id):
        print(id)
        track = sp.track(id)
        songName = track["name"]
        artist = track["artists"][0]["name"]
        album_type = track["album"]["album_type"]
        release = track["album"]["release_date"]
        release = release.split("-")
        release = f"{release[1]}-{release[2]}-{release[0]}"
        num_tracks = track["album"]["total_tracks"]
        art = track["album"]["images"][0]["url"]
        dis_num = track["track_number"]
        popularity = track["popularity"]
        explicit = track["explicit"]

        features = sp.audio_features(id)
        features = features[0]
        acousticness = features["acousticness"]
        duration = features["duration_ms"] / 1000
        time = f"{features['time_signature']}/4"
        tempo = features["tempo"]
        valence = features["valence"]

        songDetail = {
            "name": songName,
            "artist": artist,
            "art": art,
            "album_type": album_type,
            "release": release,
            "num_tracks": num_tracks,
            "dis_num": dis_num,
            "popularity": popularity,
            "explicit": explicit,
            "acousticness": acousticness,
            "duration": duration,
            "time_signature": time,
            "tempo": tempo,
            "valence": valence
        }
 
        # Writing to sample.json
        #with open("output.json", "w") as outfile:
        #    outfile.write(json_object)
        return songDetail
    
class songtoDB(Resource):
    def post(self):
        conn = sqlite3.connect("static\database\song.sqlite", check_same_thread=False)
        cursor = conn.cursor()

        json_data = request.get_json(force=True)
        trackID = json_data['trackID']
        happy_sad = json_data['happy-sad']
        calm_upbeat = json_data['calm-upbeat']
        songName = json_data["songName"]

        happy = 0
        sad = 0
        upbeat = 0
        calm = 0

        if happy_sad == "happy":
            happy += 1

        elif happy_sad == "sad":
            sad += 1

        if calm_upbeat == "calm":
            calm += 1

        elif calm_upbeat == "upbeat":
            upbeat += 1

        print(happy, sad, calm, upbeat)

        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime(f"%d")

        cursor.execute(f"""insert into SONG VALUES ('{year}-{month}-{day}', {year}, {month}, {day}, '{songName}', '{trackID}', {happy}, {sad}, {upbeat}, {calm})""")
        
        conn.commit()
        conn.close()

        return {"200": "success"}
    
api.add_resource(serachSong, "/search/<string:search>")
api.add_resource(detail, "/detail/<string:id>")
api.add_resource(songtoDB, "/songToDB/")

@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html')

@app.route("/song")
def song():
    return render_template("song.html")


if __name__ == "__main__":
    app.run(debug=True, host=HOST)
