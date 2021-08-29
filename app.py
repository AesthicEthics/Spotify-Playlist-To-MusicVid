import os
from sys import path
import requests 
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import VideosSearch as vs
import time 
import progressbar
import vlc 
import pafy 
import urllib.request
import random


client_id1 = "REDACTED"
client_secret1 = "REDACTED"
scope1 = "user-top-read"
redirect_uri = "REDACTED"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id1, client_secret=client_secret1, redirect_uri=redirect_uri, scope=scope1))

playlist_input = str(input("Playlist Link: ").strip())
playlist_id = playlist_input[-42:]

x = sp.playlist_items(playlist_id)
tracks = []
artist = []

for songs in x['tracks']['items']:
    tracks.append(str(json.dumps(songs['track']['name'], indent=4)))
    artist.append(str((json.dumps(songs['track']['artists'][0]['name'], indent=4))))

music = []

for i in range(len(artist)):
    track_x = str(tracks[i])
    artist_x = str(artist[i])
    music_x = f"{track_x} - {artist_x}"
    music_x = music_x.replace('"','')
    music.append(music_x)

song_links = []
song_ids = []

print("[+] Grabbing Song IDs")

count = 0 
path = (os.getcwd())
playlist_new = ''.join(filter(str.isalnum, playlist_id))

for root, dirs, files in os.walk(path):
    if (f"{playlist_new}.txt") in files:
        f = open(f"Database/{playlist_new}.txt",'r')
        lines = f.readlines()
        f.close()
        for i in range(len(lines)):
            if "\n" in lines[i]:
                lines[i] = lines[i].strip("\n")
        print('\n')
        print("[+] Looks like a favourite! Loading from database...")
        break


    
    else:

        for i in progressbar.progressbar(range(len(music))):

            search = vs(music[i],limit=1)

            search_results = search.result()

            for searched_song in search_results['result']:
                song_id = searched_song['id']
            f = open(f"Database/{playlist_new}.txt", "a")
            f.write(song_id)
            if (i+1) < len(music):
                f.write('\n')
            f.close()
            song_ids.append(song_id)
            time.sleep(0.02)
    
        break


print('\n')

print('[+] Generating Video Links')

for i in progressbar.progressbar(range(len(song_ids))):
    video_link = f'https://www.youtube.com/watch?v={song_ids[i]}'
    song_links.append(video_link)


shuffle = input("[+] Ready To Vibe! Would you like to shuffle? (y) or (n):  ")



if shuffle == 'y':
   random.shuffle(song_links)
    

for i in range(len(song_links)):
    url = song_links[i]
    try:
        video = pafy.new(url)
    except KeyError:
        pass
    best = video.getbest()
    playurl = best.url
    ins = vlc.Instance()
    player = ins.media_player_new()

    code = urllib.request.urlopen(url).getcode()


    Media = ins.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
  

    good_states = ["State.Playing", "State.NothingSpecial", "State.Opening"]
    while str(player.get_state()) in good_states:
        x  = 1
        time.sleep(2)
        next = input(f"Press N to move to the next song: ")
        if next == "n" or next == "N":
            break
    player.stop()
