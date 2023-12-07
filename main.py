from flask import Flask, render_template
from flask_restful import Api, Resource
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os

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

class HelloWorld(Resource):
    def get(self, search):
        top_artists = sp.current_user_top_artists(limit=5, time_range="medium_term")
        return top_artists
    
api.add_resource(HelloWorld, "/hello/<string:search>")

@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host="192.168.4.44")
