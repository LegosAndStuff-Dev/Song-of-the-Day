from flask import Flask, render_template
from flask_restful import Api, Resource
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os
import json

load_dotenv()

USERNAME = os.getenv("USERNAME")
SCOPE = os.getenv("SCOPE")
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

token = util.prompt_for_user_token(USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=SECRET, redirect_uri=REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)

app = Flask(__name__)
api = Api(app)

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
 
        # Writing to sample.json
        #with open("output.json", "w") as outfile:
        #    outfile.write(json_object)
        #return search
    
api.add_resource(serachSong, "/search/<string:search>")
api.add_resource(detail, "/detail/<string:id>")

@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host="192.168.4.44")
