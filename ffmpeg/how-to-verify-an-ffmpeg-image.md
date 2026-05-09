```
ubuntu2404
        Build
$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-7.1-ubuntu2404-desktop-build docker-images/7.1/ubuntu2404
        Run
$ docker run -it --rm --entrypoint=bash --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest

ubuntu2404-edge
        Build
$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-7.1-ubuntu2404-edge-desktop-build docker-images/7.1/ubuntu2404-edge
        Run
$ docker run -it --rm --entrypoint=bash --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-edge-desktop-build:latest

nvidia2204
vaapi2404

$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-7.1-alpine320-desktop-build docker-images/7.1/alpine320
$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-7.1-scratch320-desktop-build docker-images/7.1/scratch320



```

1: simply run the image: `docker run -it --rm --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest` 
2: now run the image in bash `docker run -it --rm --entrypoint=bash --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest`
   ffmpeg
   ffmpeg -h
   ldd `which ffmpeg`
   for i in ogg amr vorbis theora mp3lame opus vpx xvid fdk x264 x265;do echo $i; find /usr/local/ -name *$i*;done
   ffmpeg -buildconf
3: Convert an avi file to an mp4 file.
   `docker run --rm -v $(pwd):$(pwd) -w $(pwd) --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest -i drop_video_1.avi outfile/dv_converted.mp4`
4: Convert a asf file to an mp4
   `docker run --rm -v $(pwd):$(pwd) -w $(pwd) --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest -i MU_2_Discharge_Bottle___Inlet_to_Discharge.asf outfile/mpu2_discharge_bottle_converted.mp4`

```
docker run -it --rm --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest 
docker run -it --rm --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-alpine320-desktop-build:latest 

Convert an avi file to an mp4 file.
docker run -v $(pwd):$(pwd) -w $(pwd) --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest -i drop_video_1.avi dv_converted.mp4
docker run -it --rm -v $(pwd):$(pwd) -w $(pwd) --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest 
docker run -it --rm -v $(pwd):$(pwd) -w $(pwd) --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest -i MU_2_Discharge_Bottle___Inlet_to_Discharge.asf mpu2_discharge_bottle_converted.mp4

```

## kvazaar https://github.com/ultravideo/kvazaar
# RUN \
#         echo "Building kvazaar-${KVAZAAR_VERSION}" && \
export KVAZAAR_VERSION=2.0.0; export DIR=/tmp/kvazaar; export PREFIX="/opt/ffmpeg"
mkdir -p ${DIR}; cd ${DIR}
curl -sLO https://github.com/ultravideo/kvazaar/archive/v${KVAZAAR_VERSION}.tar.gz
tar -zx --strip-components=1 -f v${KVAZAAR_VERSION}.tar.gz && \
./autogen.sh
./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}



dpkg -L libaom-dev 
/.
/usr
/usr/include
/usr/include/aom
/usr/include/aom/aom.h
/usr/include/aom/aom_codec.h
/usr/include/aom/aom_decoder.h
/usr/include/aom/aom_encoder.h
/usr/include/aom/aom_external_partition.h
/usr/include/aom/aom_frame_buffer.h
/usr/include/aom/aom_image.h
/usr/include/aom/aom_integer.h
/usr/include/aom/aomcx.h
/usr/include/aom/aomdx.h
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/libaom.a
/usr/lib/x86_64-linux-gnu/pkgconfig
/usr/lib/x86_64-linux-gnu/pkgconfig/aom.pc
/usr/share
/usr/share/doc
/usr/share/doc/libaom-dev
/usr/share/doc/libaom-dev/copyright
/usr/lib/x86_64-linux-gnu/libaom.so
/usr/share/doc/libaom-dev/changelog.Debian.gz

export FFMPEG_VERSION=7.1; export DIR=/tmp/ffmpeg
export MAKEFLAGS="-j2"; PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig"
export PREFIX="/opt/ffmpeg"; LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"
mkdir -p ${DIR} && cd ${DIR}
curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2
tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2
./configure     --disable-debug  --disable-doc    --disable-ffplay   --enable-shared --enable-gpl  --extra-libs=-ldl

./configure \
--disable-debug \
        --disable-doc \
        --disable-ffplay \
        --enable-fontconfig \
        --enable-gpl \
        --enable-libaom \
        --enable-libaribb24 \
        --enable-libass \
        --enable-libbluray \
        --enable-libdav1d \
        --enable-libfdk-aac \
        --enable-libfreetype \
        --enable-libkvazaar \
        --enable-libmp3lame \
        --enable-libopencore-amrnb \
        --enable-libopencore-amrwb \
        --enable-libopenjpeg \
        --enable-libopus \
        --enable-libsrt \
        --enable-libsvtav1 \
        --enable-libtheora \
        --enable-libvidstab \
        --enable-libvmaf \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libwebp \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libxvid \
        --enable-libzimg \
        --enable-libzmq \
        --enable-nonfree \
        --enable-openssl \
        --enable-postproc \
        --enable-shared \
        --enable-small \
        --enable-version3 \
        --extra-cflags="-I${PREFIX}/include" \
        --extra-ldflags="-L${PREFIX}/lib" \
        --extra-libs=-ldl \
        --extra-libs=-lm \
        --extra-libs=-lpthread \
        --ld=g++ \
        --prefix="${PREFIX}"