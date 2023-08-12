import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"

SPOTIFY_CLIENT_ID = MY_SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = MY_SPOTIFY_CLIENT_SECRET

target_date_info = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(URL + target_date_info)
webpage_html = response.text

soup = BeautifulSoup(webpage_html, "html.parser")

song_titles = [item.getText().strip() for item in soup.select("li h3")]
song_top100_titles = song_titles[:100]
print(song_top100_titles)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()["id"]
print(user_id)

# Searching Spotify for songs by title
song_uris = []
year = target_date_info.split("-")[0]
for song in song_top100_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{target_date_info} Billboard 100", public=False)
# print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print("Done to add")