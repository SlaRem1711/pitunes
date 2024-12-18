import spotipy #scraping spotify library#
import sys
import os
import time
import requests 
from io import BytesIO
from PIL import Image       #           for my           #
from PIL import ImageDraw   #                            #
from PIL import ImageFont   #           Display          #
import st7735
from spotipy.oauth2 import SpotifyClientCredentials

def display_image_url(url):
	response=requests.get(url)
	image = Image.open(BytesIO(response.content))
	image=image.resize((120,141))
	disp.set_window(0, 20)
	disp.display(image)
	disp.set_window()
	
def Track_Name(Name,positionm):
	txt = Image.new('RGB', (WIDTH, HEIGHT))
	draw = ImageDraw.Draw(txt)
	font = ImageFont.load_default()
	draw.text((5, 5),'#' + str(positionm) +': '+ Name, font=font,fill=(255, 255, 255))
	disp.display(txt)


disp = st7735.ST7735(port=0, cs=0, dc=25, backlight=None,rst=24, width=120, height=161, rotation=180, invert=False)
WIDTH = disp.width
HEIGHT = disp.height
img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)
draw.rectangle((0,0,WIDTH, HEIGHT), (0,0,0))

# Load default font.
font = ImageFont.load_default()
line_skip = 0

auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)

while True:
	
	artist_name = input('Enter the artist name: ')
		
	results = spotify.search(q='artist:' + artist_name, type='artist')
	items = results['artists']['items']
	if len(items) > 0:
		artist = items[0]
		
		print(artist['name'], artist['uri'])

	artist_uri = artist['uri']

	#ALBUMS 

	#results = spotify.artist_albums(artist_uri, album_type='album')
	#albums = results['items']

	#while results['next']:
	#	results = spotify.next(results)
	#	albums.extend(results['items'])

	#for album in albums:
	#	draw.text((5, line_skip), album['name'], font=font,fill=(255, 255, 255))
	#	line_skip+=12

	#TOP TRACKS
	results = spotify.artist_top_tracks(artist_uri)	
	pos = 5
	for track in results['tracks'][:5][::-1]:
		song = track['name']
		Track_Name(song, pos)
		album_cover = track['album']['images'][0]['url']
		display_image_url(album_cover)
		
		pos -= 1
		time.sleep(5)
		draw.rectangle((0,0,WIDTH, HEIGHT), (0,0,0))


	disp.display(img)	

