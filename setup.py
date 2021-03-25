from setuptools import find_packages, setup

setup(
    name="spotifyutils",
    version="0.2",
    py_modules="spotifyutils",
    packages=find_packages("."),
    #package_dir={"": "."},
    install_requires=[
        "Click",
        "pyyaml",
        "spotipy"
    ],
    entry_points={
        "console_scripts": ["spotifyutils=spotifyutils:cli"]
    }
)
