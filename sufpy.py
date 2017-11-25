#/Users/greglewis/anaconda/bin/python
# -*- coding: utf-8 -*-

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from twython import Twython
import random, yaml
import os
import time

# delay execution of script by up to 1 hour, randomly
start_delay = random.randint(0,3600)
time.sleep(start_delay)

# load yaml file with Twtter & Spotify keys
config = yaml.load(open("config.yaml"))

# Authorize with Twitter
twitter_app_key = config['twitter_app_key']
twitter_app_secret = config['twitter_app_secret']
twitter_oauth_token = config['twitter_oauth_token']
twitter_oauth_token_secret = config['twitter_oauth_token_secret']
twitter = Twython(twitter_app_key, twitter_app_secret, twitter_oauth_token, twitter_oauth_token_secret)

# Authorize with Spotify
os.environ["SPOTIPY_CLIENT_ID"] = config["SPOTIPY_CLIENT_ID"]
os.environ["SPOTIPY_CLIENT_SECRET"] = config["SPOTIPY_CLIENT_SECRET"]
os.environ["SPOTIPY_REDIRECT_URI"] = config["SPOTIPY_REDIRECT_URI"]                      
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Start the Sufjan fun! With Sufjan!
sufjan = {}
key_counter = 0
SilverAndGold = '0AVvBrOZ4Hy3yCW8SguJLy'
SongsForChristmas = '6ZCbYO3B5eslkY3zHdss4A'

# Function iterates through an album and grabs song name & URI
def get_sufjan(album,song_list,counter):
    for i, t in enumerate(album['items']):
        song_list[counter] = [t['name'], t['external_urls']['spotify']]
        counter += 1    

# Connect to Spotify and gets song info for every track on both albums
# Limitted to 50 tracks/request, so S&G is split across two vars
SFC = sp.album_tracks(SongsForChristmas, limit=50, offset=0)
SandG1 = sp.album_tracks(SilverAndGold, limit=50, offset=0)
SandG2 = sp.album_tracks(SilverAndGold, limit=50, offset=50)
albums = [SFC,SandG1,SandG2]

# Run the function on the albums to get the full list of tracks to use
# key:value
# Int:[Song Name, URI]
for item in albums:
    get_sufjan(item,sufjan,key_counter)

# Pick a random track and Tweet it!!
song_number = random.randint(0,99)
song = sufjan[song_number]
if song[0] == "Christmas Unicorn":
    tweet = song[0]+ "🎄🦄 " + song[1]
else:
    tweet = song[0]+ " " + song[1]

twitter.update_status(status=tweet)
