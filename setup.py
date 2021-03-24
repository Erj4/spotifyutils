from setuptools import setup

setup(
    name="spotifyutils",
    version="0.1",
    py_modules="spotifyutils",
    install_requires=[
        "Click",
        "pyyaml",
        "spotipy"
    ],
    entry_points='''
        [console_scripts]
        spotifyutils=spotifyutils:cli
    '''
)
