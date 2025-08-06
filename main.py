
from spotipy import Spotify, SpotifyOAuth
import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow


def get_spotify_songs(playlist_id,sp):
    results = sp.playlist_items(playlist_id)
    tracks=results['items']
    songs = {}
    for track in tracks:
        songs[track['track']['name']] = track['track']['artists'][0]['name']
    print(songs)
    return songs


def get_youtube_credentials():
    """Get YouTube OAuth credentials"""
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    creds = None
    
    # Load existing credentials if available
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def find_youtube_songs_and_create_playlist(songs, playlist_name):
    """Find YouTube videos and create a playlist"""
    creds = get_youtube_credentials()
    youtube = build("youtube", "v3", credentials=creds)
    
    # Create a new playlist
    playlist_response = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": playlist_name,
                "description": f"Playlist created from Spotify: {playlist_name}",
                "privacyStatus": "private"
            }
        }
    ).execute()
    
    playlist_id = playlist_response['id']
    print(f"Created YouTube playlist: {playlist_name}")
    print(f"Playlist URL: https://www.youtube.com/playlist?list={playlist_id}")
    print()
    
    video_ids = []
    total_songs = len(songs)
    songs_found = 0
    
    for song_name, artist_name in songs.items():
        search_query = f"{song_name} {artist_name}"
        search_response = youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            maxResults=1
        ).execute()
        
        if search_response['items']:
            songs_found += 1
            video = search_response['items'][0]
            video_id = video['id']['videoId']
            video_ids.append(video_id)
            print(f"Found {songs_found} of {total_songs} songs")
            print(f"Found: {video['snippet']['title']} - {video['snippet']['channelTitle']}")
            print(f"URL: https://www.youtube.com/watch?v={video_id}")
        else:
            print(f"No video found for: {search_query}")
        print()
    
    # Add videos to playlist
    print("Adding videos to playlist...")
    for video_id in video_ids:
        try:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print(f"Added video to playlist")
        except Exception as e:
            print(f"Error adding video {video_id}: {e}")
    
    print(f"\nPlaylist creation complete! Check your YouTube account.")
    return playlist_id


def main():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json",  # Your OAuth2 client config file
        scopes=scopes
    )
    flow.run_local_server(port=8080)

    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))
    
    print("Please enter your Spotify playlist link:")
    playlist_link = input()
    playlist_id = playlist_link.split("/")[-1].split("?")[0]
    
    print("Please enter a name for your YouTube playlist:")
    playlist_name = input()
    
    songs = get_spotify_songs(playlist_id, sp)
    find_youtube_songs_and_create_playlist(songs, playlist_name)
if __name__ == "__main__":
    # This block ensures that main() is called only when the script is executed directly
    main()




