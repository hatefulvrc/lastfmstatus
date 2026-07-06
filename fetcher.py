import requests
import json
import time

API_KEY = "e45f558d30f6e21d1858f99e6a78bf94"
USER = "lucidily"
URL = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USER}&api_key={API_KEY}&format=json&limit=1"

def update_status():
    try:
        response = requests.get(URL).json()
        track = response['recenttracks']['track'][0]
        # Check if currently playing
        is_playing = '@attr' in track and track['@attr'].get('nowplaying') == 'true'

        data = {
            "name": "Kasahi",
            "status": "playing" if is_playing else "offline",
            "track": track['name'] if is_playing else None,
            "artist": track['artist']['#text'] if is_playing else None
        }

        with open("status.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error fetching data: {e}")

# Run loop every 120 seconds
while True:
    update_status()
    time.sleep(120)
