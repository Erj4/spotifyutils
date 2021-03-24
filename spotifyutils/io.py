import click
import spotipy

from spotifyutils.buffered import auto_paginate


def select_playlist(config, spotify):
    playlists = {
        playlist["name"]: playlist
        for playlist in auto_paginate(spotify, spotify.current_user_playlists())
    }

    if "playlist" in config:
        return playlists[config["playlist"]]["id"]

    selected_playlist = click.prompt(
        "Playlist to like", type=click.Choice(playlists))

    click.echo("{playlist} has {song_count} song(s)".format(
        playlist=selected_playlist,
        song_count=playlists[selected_playlist]["tracks"]["total"]
    ))

    return playlists[selected_playlist]["id"]
