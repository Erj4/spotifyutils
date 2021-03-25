import spotipy
import typing


class BufferedFunction():
    _items = []

    def __init__(self, func: typing.Callable, limit: int):
        self.limit = limit
        self.func = func

    def __call__(self, x):
        self.add(x)

    def add(self, x):
        self._items.append(x)

        if len(self._items) >= self.limit:
            self.flush()

    def flush(self):
        self.func(self._items)
        self._items = []

    def __enter__(self):
        self._items = []

    def __exit__(self, error_type, error_value, error_traceback):
        self.flush()


def auto_paginate(spotify: spotipy.Spotify, paginated):
    while True:
        for item in paginated["items"]:
            yield item

        if paginated["next"]:
            paginated = spotify.next(paginated)
        else:
            break
