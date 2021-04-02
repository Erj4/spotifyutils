import asyncio
import click
import discord
import yaml

from spotifyutils.buffered import auto_paginate, BufferedFunction
from spotifyutils.connection import get_connection


@click.group()
@click.option("--cred-file", "--credentials-file", "-c", default="credentials.yaml")
@click.option("--callback-url", "--url", default="http://localhost:30001")
@click.option("--discord-user-id", "--discord-user", required=False)
@click.pass_context
def cli(ctx, cred_file, callback_url, discord_user_id):
    with click.open_file(cred_file) as f:
        credentials = yaml.safe_load(f)

    if "spotify" not in credentials:
        raise click.exceptions.ClickException(
            f"Spotify credentials missing from credential file '{cred_file}'")

    if "id" not in credentials["spotify"]:
        raise click.exceptions.ClickException(
            f"Spotify id missing from credential file '{cred_file}'")

    if "secret" not in credentials["spotify"]:
        raise click.exceptions.ClickException(
            f"Spotify secret missing from credential file '{cred_file}'")

    async def discord_send_auth_request(credentials, user_id, url):
        if "discord" not in credentials:
            raise click.exceptions.ClickException(
                f"Discord credentials missing from credential file '{cred_file}'")
        if "token" not in credentials["discord"]:
            raise click.exceptions.ClickException(
                f"Discord token missing from credential file '{cred_file}'")

        client = discord.Client()
        try:
            await client.login(credentials["discord"]["token"])
            user = await client.fetch_user(user_id)
            await user.send(f"Spotify utils needs you to authorise:\n{url}")
        finally:
            if not client.is_closed():
                await client.close()

    def send_auth_request(url):
        if discord_user_id is not None:
            asyncio.run(discord_send_auth_request(
                credentials, discord_user_id, url))

    ctx.obj = get_connection(
        credentials["spotify"]["id"],
        credentials["spotify"]["secret"],
        send_auth_request,
        callback_url
    )


def get_user_playlist_id(spotify, name):
    if name is None:
        return None

    playlists = {
        playlist["name"]: playlist
        for playlist in auto_paginate(spotify, spotify.current_user_playlists())
    }

    if name not in playlists:
        raise click.exceptions.UsageError(
            f"Playlist {name} isn't one of your playlists\nShould be one of: {list(playlists.keys())}"
        )

    playlist = playlists[name]
    length = playlist["tracks"]["total"]

    click.echo(f"Playlist {name} has {length} song(s)")

    return playlist["id"]


@cli.command()
@click.option(
    "--playlist",
    "-p",
    "playlist_id",
    required=False,
    callback=lambda ctx, _, value: get_user_playlist_id(ctx.obj, value)
)
@click.option("--interactive", "-i", is_flag=True)
@click.pass_obj
def like_playlist(spotify, playlist_id, interactive):
    playlist_names = [
        playlist["name"] for playlist
        in auto_paginate(spotify, spotify.current_user_playlists())
    ]

    if playlist_id is None:
        playlist = click.prompt(
            "Playlist to like", type=click.Choice(playlist_names)
        )

        playlist_id = get_user_playlist_id(spotify, playlist)

    songs_result = spotify.playlist_tracks(playlist_id)

    buffered_save_track = BufferedFunction(
        spotify.current_user_saved_tracks_add,
        50
    )

    with buffered_save_track:
        with click.progressbar(auto_paginate(spotify, songs_result)) as songs:
            for song in songs:
                track = song["track"]

                if interactive:
                    prompt_text = "Title:\t{title}\nArtist:\t{artist}\nAlbum:\t{album}".format(
                        title=track["name"],
                        artist=", ".join(
                            map(lambda artist: artist["name"], track["artists"])),
                        album=track["album"]["name"]
                    )
                    click.secho(prompt_text, fg='green', err=True)

                if not interactive or click.confirm("Add to library?", default=True, err=True):
                    buffered_save_track(track["id"])
