docker build -t ffmpeg-devel:latest .

docker run ffmpeg-devel:latest
docker run -it --rm --entrypoint=bash ffmpeg-devel:latest

docker tag ffmpeg-devel:1.0