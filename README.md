# MusicDownloaderServer

Build the container:

``` bash
docker build -t conikolg/music-dl-server:v$VERSION .
docker tag conikolg/music-dl-server:v$VERSION conikolg/music-dl-server:latest
```

Delete all untagged container images:

``` bash
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
