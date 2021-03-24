from spotipy import Spotify, SpotifyOAuth


def get_connection(client_id, client_secret):
    scope = "user-library-modify,user-library-read,playlist-read-private,user-read-private,user-read-email"

    auth_manager = SpotifyOAuth(
        client_id, client_secret, "http://localhost:30001", scope=scope
    )
    return Spotify(auth_manager=auth_manager)
