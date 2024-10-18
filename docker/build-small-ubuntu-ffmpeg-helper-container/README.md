docker build -t small-ffmpeg:latest .

docker run small-ffmpeg:latest
docker run -it --rm --entrypoint=bash small-ffmpeg:latest