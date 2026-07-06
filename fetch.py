import requests
import json
import os

# Get the API Key from the environment variable set in GitHub Actions
API_KEY = os.environ.get("LASTFM_API_KEY")
USER = "lucidily"
URL = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USER}&api_key={API_KEY}&format=json&limit=1"

def update_status():
    try:
        response = requests.get(URL).json()
        
        # Safely access the track list
        tracks = response.get('recenttracks', {}).get('track', [])
        if not tracks:
            return

        track = tracks[0]
        
        # Check if currently playing
        is_playing = '@attr' in track and track['@attr'].get('nowplaying') == 'true'
        
        data = {
            "name": "hatefulvrc",
            "status": "playing" if is_playing else "offline",
            "track": track['name'] if is_playing else None,
            "artist": track['artist']['#text'] if is_playing else None
        }
        
        # Save to file
        with open("status.json", "w") as f:
            json.dump(data, f, indent=4)
            
        print("Status successfully updated.")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    update_status()
