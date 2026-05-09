FROM        ubuntu:24.04 AS base

WORKDIR     /tmp/workdir

# if running in the `run --rm -v $(pwd):$(pwd) -w $(pwd) ` then comment out the following COPY lines
# otherwise, uncomment them
COPY generate-source-of-truth-ffmpeg-versions.py /tmp/workdir
COPY download_tarballs.sh /tmp/workdir
COPY build_source.sh /tmp/workdir

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends curl jq python3 python3-requests less tree && \
        chmod +x /tmp/workdir/download_tarballs.sh && \
        chmod +x /tmp/workdir/build_source.sh


RUN \
        python3 /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --mode manifest --output generated_build_manifest.json

RUN \
        /tmp/workdir/download_tarballs.sh

ARG         PREFIX="/opt/ffmpeg"

RUN \
        /tmp/workdir/build_source.sh
