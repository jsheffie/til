docker build -t ffmpeg-tarballs-download:latest .

docker build --no-cache -t ffmpeg-tarballs-download:latest .

docker run ffmpeg-tarballs-download:latest

docker run -it --rm --entrypoint=bash ffmpeg-tarballs-download:latest

While developing the script... its much easier to loopback mount the things.
docker run --rm -v $(pwd):$(pwd) -w $(pwd) -it --rm --entrypoint=bash ffmpeg-tarballs-download:latest

foo



This is what inspired the event ( download tarballs )
https://stackoverflow.com/a/56333947/1184492
https://pastebin.com/jWNbhUBd