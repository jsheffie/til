import requests
import json

"""
To run this script you need the requests library. You can install it with pip:
in a venv as follows:

$ python3 -mvenv .venv
$ source .venv/bin/activate
$ pip install requests
$ python3 ./generate-ffmpeg-support-libs-table.py > list_of_recent_images.txt
$ deactivate
$ rm -rf .venv

you will now have a file called list_of_recent_images.txt with the list of images
"""

LIBRARIES = {
    "nasm": { "link": "https://www.nasm.us/", 
             "ffmpeg_wiki_build_instructions": "https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu" },
    "opencore-amr": { "link": "https://sourceforge.net/projects/opencore-amr/" },
    "libx264": { "link": "https://www.videolan.org/developers/x264.html" },
    "libx265": { "link": "https://bitbucket.org/multicoreware/x265" },
    "libogg": { "link": "https://xiph.org/ogg/" },
    "libopus": { "link": "https://opus-codec.org/" },
    "libvorbis": { "link": "https://xiph.org/vorbis/" },
    "libvpx": { "link": "https://www.webmproject.org/code/" },
    "libwebp": { "link": "https://developers.google.com/speed/webp/" },
    "libmp3lame": { "link": "https://lame.sourceforge.io/" },
    "libxvidcore": { "link": "https://www.xvid.com/" },
    "libdav1d": { "link": "https://code.videolan.org/videolan/dav1d" },
    "libtheora": { "link": "https://www.theora.org/" },
    "xvid": { "link": "https://www.xvid.com/" },
    "libfdk-aac": { "link": "" },
    "libaom": { "link": "https://aomedia.org/" },
    "libsvtav1": { "link": "" },
    "kvazaar": { "link": "" },
    "libvmaf": { "link": "" },
    "FFmpeg": { "link": "https://ffmpeg.org/" }
}
def make_api_request(page, page_size):
    url = "https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/tags"
    params = {"page": page, "page_size": page_size}
    response = requests.get(url, params=params)
    return response.json()

def process_data(data):
    data = json.loads(data)
    sorted_data = sorted(data, key=lambda x: x["name"], reverse=True)
    for item in sorted_data:
        if item["tag_status"].lower() == "active":
            size_mb = round(item["full_size"] / 1048576)
            name_padding = " " * (20 - len(item["name"]))
            size_padding = " " * (8 - len(str(size_mb)))
            last_updated = item["last_updated"][:10]
            # print("-" * 50)
            # print(json.dumps(item, indent=4))
            print(f"{item['name']}{name_padding}{size_mb}mb{size_padding}{last_updated}")
            # print(f'{item["last_updater_username"]}')

def main():
    page = 1
    page_size = 100
    data = []

    while True:
        response = make_api_request(page, page_size)
        data.extend(response["results"])

        if len(response["results"]) < page_size:
            break

        page += 1

    process_data(json.dumps(data))

if __name__ == "__main__":
    main()