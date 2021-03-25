# Spotify Utils

## Building

Build using the following command (replacing `VERSION` with the desired version tag):
`docker buildx build . -t xor110/spotifyutils:v<VERSION> --platform linux/arm/v7,linux/arm64/v8,linux/amd64 --push`
