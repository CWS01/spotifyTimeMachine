import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "cca0cc455fc242e68ca820d04eaf72c4"
SPOTIPY_CLIENT_SECRET = "c8b27c0ceaa44a0783aa35f643956af6"
SPOTIPY_REDIRECT_URI = "http://example.com"

travel_to_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

url = f"https://www.billboard.com/charts/hot-100/{travel_to_date}"

response = requests.get(url)
billboard_website = response.text

soup = BeautifulSoup(billboard_website, "html.parser")
song_titles = soup.select("li ul li h3")
songs = [song.getText().strip() for song in song_titles]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True,
                                               username="cws1067"))

id = sp.current_user()["id"]
year = travel_to_date.split("-")[0]
song_uris = []
for song in songs:
    try:
        song_details = sp.search(q=f"track: {song} year: {year}", type="track")["tracks"]["items"][0]["uri"]
        song_uris.append(song_details)
    except IndexError:
        print("No Song was Found")

new_playlist = sp.user_playlist_create(user=id,
                                       name=f"{travel_to_date} Billboard 100",
                                       public=False,
                                       description="Playlist created based on a specific date inputted")

playlist_id = new_playlist["id"]

# Adds tracks specifiefd in the song URIs list to the playlist created above
sp.playlist_add_items(
    playlist_id=playlist_id,
    items=song_uris,
)
