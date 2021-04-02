from setuptools import find_packages, setup

setup(
    name="spotifyutils",
    version="0.2",
    py_modules="spotifyutils",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "Click",
        "pyyaml",
        "spotipy",
        "discord"
    ],
    entry_points={
        "console_scripts": ["spotifyutils=spotifyutils:cli"]
    }
)
