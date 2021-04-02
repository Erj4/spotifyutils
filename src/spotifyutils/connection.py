import click

from spotipy import Spotify, SpotifyOAuth
from spotipy.oauth2 import start_local_http_server


def get_connection(client_id, client_secret, send_auth_request, callback_url):
    scope = "user-library-modify,user-library-read,playlist-read-private,user-read-private,user-read-email"

    auth_manager = SpotifyOAuth(
        client_id, client_secret, callback_url, scope=scope, open_browser=False
    )

    url = auth_manager.get_authorize_url()
    click.echo(f"Auth URL: {url}")

    if auth_manager.get_cached_token() is None:
        send_auth_request(url)
        start_local_http_server(30001)

    return Spotify(auth_manager=auth_manager)
