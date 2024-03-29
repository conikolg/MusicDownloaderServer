# MusicDownloaderServer

Prepare the container:

``` bash
# Build the new container
docker build -t conikolg/music-dl-server:v$VERSION .
# Tag it as the latest one
docker tag conikolg/music-dl-server:v$VERSION conikolg/music-dl-server:latest
# Delete all untagged container images:
docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc)
```

Run the container:

``` bash
# Attached, delete on exit
docker run -it --rm \
    -p 8100:8100 \
    -e SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID \
    -e SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET \
    conikolg/music-dl-server
# Unattached, persist on exit
docker run -itd \
    -p 8100:8100 \
    --name music-dl-server \
    -e SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID \
    -e SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET \
    conikolg/music-dl-server
```
