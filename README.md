# Spotify to YouTube Playlist Maker

This application allows users to convert their Spotify playlists to YouTube playlists by searching for each song on YouTube and creating a new playlist with the found videos.

## Features

- Extract songs from Spotify playlists
- Search for songs on YouTube
- Create YouTube playlists with found videos
- OAuth2 authentication for YouTube (no API key needed for playlist creation)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Spotify Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Get your `CLIENT_ID` and `CLIENT_SECRET`
4. Add them to your `.env` file:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

### 3. YouTube OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **YouTube Data API v3**
4. Go to "Credentials" and create OAuth 2.0 Client ID
5. Choose "Desktop application" as the application type
6. Download the JSON file and rename it to `client_secrets.json`
7. Place `client_secrets.json` in the same directory as `main.py`

### 4. First Run

When you run the script for the first time:
1. A browser window will open for YouTube authentication
2. Sign in with your Google account
3. Grant permissions to manage your YouTube playlists
4. The credentials will be saved in `token.pickle` for future use

## Usage

```bash
python main.py
```

The script will:
1. Ask for your Spotify playlist link
2. Ask for a name for your YouTube playlist
3. Extract songs from Spotify
4. Search for each song on YouTube
5. Create a new YouTube playlist and add the found videos

## Files

- `main.py` - Main application
- `client_secrets.json` - YouTube OAuth credentials (you need to download this)
- `token.pickle` - Saved authentication token (created automatically)
- `.env` - Environment variables for Spotify credentials
- `requirements.txt` - Python dependencies

## Notes

- YouTube playlists are created as private by default
- The app searches for the first video result for each song
- Authentication tokens are saved locally for convenience
- You can delete `token.pickle` to force re-authentication 