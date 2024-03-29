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

from database import getNumCalm, getNumHappy, getNumSad, getNumUpbeat
from id import makeID

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
        token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

        if token:
            sp = spotipy.Spotify(auth=token)

        search = sp.search(q=search, type="track", limit=6)
        json_object = json.dumps(search, indent=4)
 
        # Writing to sample.json
        with open("output.json", "w") as outfile:
            outfile.write(json_object)
        return search
    
class detail(Resource):
    def get(self, id):
        print(id)
        token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

        if token:
            sp = spotipy.Spotify(auth=token)

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
            "id": id,
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
        token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

        if token:
            sp = spotipy.Spotify(auth=token)

        conn = sqlite3.connect("static\database\song.sqlite")
        cursor = conn.cursor()

        json_data = request.get_json(force=True)
        trackID = json_data['trackID']
        happy_sad = json_data['happy-sad']
        calm_upbeat = json_data['calm-upbeat']

        search = sp.track(trackID)

        artist = search["artists"][0]["name"]
        if len(search["artists"]) > 1:
            artist = ""
            for i in range(len(search["artists"])):
                print(search["artists"][i]["name"])
                artist += f"{search['artists'][i]['name']}, "

            artist = artist.removesuffix(", ")


        songName = search["name"]

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

        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime(f"%d")

        id = makeID(20, True, True, True)
        print(id)
        #its the special characters making the issue
        cursor.execute(f"""insert into SONG VALUES ('{id}', '{year}-{month}-{day}', {year}, {month}, {day}, "{songName}", "{artist}", '{trackID}', 1, 0, 1, 0)""")
        
        conn.commit()
        conn.close()

        return {"200": "success"}
    
class findSong(Resource):
    def post(self):
        conn = sqlite3.connect("static\database\song.sqlite", check_same_thread=False)
        cursor = conn.cursor()

        json_data = request.get_json(force=True)
        type = json_data['type']
        search = json_data['search']

        if type == "date":
            if '-' in str(search):
                print("test")
                print(search)
                cursor.execute(f"SELECT * FROM SONG WHERE date='{search}' ORDER BY day ASC")
            else: 
                cursor.execute(f"SELECT * FROM SONG WHERE month={search} ORDER BY day ASC")

            items = cursor.fetchall()
            print(items)
            none = str(items)

            if none == "[]":
                return {"200": "success",
                        "output": None}

            else:
                return {"200": "success",
                        "output": items}

        if type == "song":
            cursor.execute(f"SELECT * FROM SONG WHERE songNAME LIKE '{search}' ORDER BY day ASC")

            items = cursor.fetchall()
            none = str(items)

            if none == "[]":
                return {"200": "success",
                        "output": None}

            else:
                return {"200": "success",
                        "output": items}      


        conn.close()

        return {"200": "success"}
    
class getTop10(Resource):
    def get(self, term):
        token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

        if token:
            sp = spotipy.Spotify(auth=token)

        if term == "1m":
            topArtist = sp.current_user_top_artists(limit=10, time_range="short_term")
            topSong = sp.current_user_top_tracks(limit=10, time_range="short_term")

            return {"artists": topArtist, "song": topSong}

        elif term == "6m":
            topArtist = sp.current_user_top_artists(limit=10, time_range="medium_term")
            topSong = sp.current_user_top_tracks(limit=10, time_range="medium_term")

            return {"artists": topArtist, "song": topSong}

        elif term == "lifetime":
            topArtist = sp.current_user_top_artists(limit=10, time_range="long_term")
            topSong = sp.current_user_top_tracks(limit=10, time_range="long_term")

            return {"artists": topArtist, "song": topSong}
        
class editClass(Resource):
    def post(self):
        conn = sqlite3.connect("static\database\song.sqlite")
        cursor = conn.cursor()

        json_data = request.get_json(force=True)
        print(json_data['id'], json_data["date"], json_data["type"], json_data["happy-sad"], json_data["calm-upbeat"])

        if json_data["type"] == "save":
            date = json_data['date']
            date2 = date.split("-")
            for i in range(len(date2)):
                date2[i] = int(date2[i])

            year = date2[0]
            month = date2[1]
            day = date2[2]

            cursor.execute(f""" Update SONG SET year=({year}) WHERE id ="{json_data['id']}" """)
            conn.commit()
            
            cursor.execute(f""" Update SONG SET month=({month}) WHERE id ="{json_data['id']}" """)
            conn.commit()
            
            cursor.execute(f""" Update SONG SET day=({day}) WHERE id ="{json_data['id']}" """)
            conn.commit()

            print(date2)

            cursor.execute(f""" Update SONG SET date="{date}" WHERE id="{json_data['id']}" """)
            conn.commit()

            if json_data["happy-sad"] == "happy":
                cursor.execute(f""" Update SONG SET happy=1 WHERE id ="{json_data['id']}" """)
                conn.commit()
                cursor.execute(f""" Update SONG SET sad=0 WHERE id ="{json_data['id']}" """)
                conn.commit()

            if json_data["happy-sad"] == "sad":
                cursor.execute(f""" Update SONG SET sad=1 WHERE id ="{json_data['id']}" """)
                conn.commit()
                cursor.execute(f""" Update SONG SET happy=0 WHERE id ="{json_data['id']}" """)
                conn.commit()

            if json_data["calm-upbeat"] == "calm":
                cursor.execute(f""" Update SONG SET calm=1 WHERE id ="{json_data['id']}" """)
                conn.commit()
                cursor.execute(f""" Update SONG SET upbeat=0 WHERE id ="{json_data['id']}" """)
                conn.commit()

            if json_data["calm-upbeat"] == "upbeat":
                cursor.execute(f""" Update SONG SET upbeat=1 WHERE id ="{json_data['id']}" """)
                conn.commit()
                cursor.execute(f""" Update SONG SET calm=0 WHERE id ="{json_data['id']}" """)
                conn.commit()

        if json_data["type"] == "delete":
            cursor.execute(f"""DELETE FROM SONG WHERE id="{json_data['id']}" """)
            conn.commit()

            

        return {"200": "success", "type": json_data["type"]}
    
class searchID(Resource):
    def get(self, id):
        token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

        if token:
            sp = spotipy.Spotify(auth=token)

        track = sp.track(id)

        print(track)
        return track
        
    
api.add_resource(serachSong, "/search/<string:search>")
api.add_resource(detail, "/detail/<string:id>")
api.add_resource(songtoDB, "/songToDB/")
api.add_resource(findSong, "/findSong/")
api.add_resource(getTop10, "/getTop/<string:term>/")
api.add_resource(editClass, "/edit/")
api.add_resource(searchID, "/id/search/<string:id>")

@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html')

@app.route("/song")
def song():
    return render_template("song.html")

@app.route("/recap")
def recap():
    token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)

    topArtist = sp.current_user_top_artists(limit=10, time_range="short_term")
    topSong = sp.current_user_top_tracks(limit=10, time_range="short_term")

    return render_template("recap.html", topArtist=topArtist, topSong=topSong)

@app.route("/archive")
def archive():
    conn = sqlite3.connect("static\database\song.sqlite")
    cursor = conn.cursor()

    month = datetime.datetime.now().strftime("%m")
    monthSpelled = datetime.datetime.now().strftime("%B")

    cursor.execute(f"SELECT * FROM SONG WHERE month='{month}' ORDER BY day ASC")

    items = cursor.fetchall()
    song = True
    none = str(items)

    if none == "[]":
        items = f"No songs in the {monthSpelled}!"
        song = False

    happy = getNumHappy(month)
    sad = getNumSad(month)

    upbeat = getNumUpbeat(month)
    calm = getNumCalm(month)

    print(happy, sad, upbeat, calm)

    return render_template("archive.html", items=items, song=song, happy=happy, sad=sad, upbeat=upbeat, calm=calm)

@app.route("/archive/edit/<string:id>")
def edit(id):
    conn = sqlite3.connect("static\database\song.sqlite")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM SONG WHERE id='{id}'""")

    items = cursor.fetchone()
    return render_template("edit.html", items=items, id=id)

@app.route("/archive/year")
def song():
    pass



if __name__ == "__main__":
    app.run(debug=True, host=HOST)
