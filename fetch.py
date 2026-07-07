import requests
import json
import os

API_KEY = os.environ.get("LASTFM_API_KEY")
USER = "lucidily"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def fetch_data():
    try:
        # 1. Get Total Scrobbles
        info_url = f"{BASE_URL}?method=user.getinfo&user={USER}&api_key={API_KEY}&format=json"
        info_res = requests.get(info_url).json()
        total_scrobbles = info_res.get('user', {}).get('playcount', "0")

        # 2. Get Top Artist (Last 7 Days)
        top_url = f"{BASE_URL}?method=user.gettopartists&user={USER}&api_key={API_KEY}&period=7day&limit=1&format=json"
        top_res = requests.get(top_url).json()
        top_artists = top_res.get('topartists', {}).get('artist', [])
        
        top_artist_name = "None"
        top_artist_plays = "0"
        
        if top_artists:
            top_artist_name = top_artists[0]['name']
            top_artist_plays = top_artists[0]['playcount']

        # 3. Get Recent Track (Now Playing Status)
        recent_url = f"{BASE_URL}?method=user.getrecenttracks&user={USER}&api_key={API_KEY}&limit=1&format=json"
        recent_res = requests.get(recent_url).json()
        tracks = recent_res.get('recenttracks', {}).get('track', [])
        
        is_playing = False
        if tracks and '@attr' in tracks[0] and tracks[0]['@attr'].get('nowplaying') == 'true':
            is_playing = True

        # Construct final data with spaces in keys
        data = {
            "Name": "hatefulvrc",
            "Scrobbles": total_scrobbles,
            "Top Artist": top_artist_name,
            "Top Plays": top_artist_plays
        }
        
        with open("status.json", "w") as f:
            json.dump(data, f, indent=4)
            
        print("Data successfully updated.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_data()
