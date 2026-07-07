import requests
import json
import os

# Configuration
API_KEY = os.environ.get("LASTFM_API_KEY")
USER = "lucidily"

def get_data():
    try:
        # 1. Fetch Recent Track
        recent_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USER}&api_key={API_KEY}&format=json&limit=1"
        recent_res = requests.get(recent_url).json()
        tracks = recent_res.get('recenttracks', {}).get('track', [])
        is_playing = False
        track_name = None
        track_artist = None
        
        if tracks:
            track = tracks[0]
            is_playing = '@attr' in track and track['@attr'].get('nowplaying') == 'true'
            if is_playing:
                track_name = track['name']
                track_artist = track['artist']['#text']

        # 2. Fetch Top Artist (Last 7 Days)
        top_artist_url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={USER}&api_key={API_KEY}&format=json&period=7day&limit=1"
        top_res = requests.get(top_artist_url).json()
        top_artist = top_res.get('topartists', {}).get('artist', [])
        top_artist_name = top_artist[0]['name'] if top_artist else "N/A"

        # 3. Construct Data
        data = {
            "name": "hatefulvrc",
            "status": "playing" if is_playing else "offline",
            "current_track": track_name,
            "current_artist": track_artist,
            "top_artist_7days": top_artist_name
        }
        
        # Save to file
        with open("status.json", "w") as f:
            json.dump(data, f, indent=4)
            
        print("Status successfully updated.")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    get_data()
