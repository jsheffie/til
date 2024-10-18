Here is the PR I was working
https://github.com/jrottenberg/ffmpeg/pull/408

```
# from 3.13 -> 3.20 
#      - initial RUN apk add
#          - removed: libcrypto1.1 libssl1.1
#          - added: openssl, zeromq
#      - buildDeps
#          - added zeromq-dev, alpine-sdk, linux-headers, freetype-dev
# try: move zeromq-dev to buildDeps
# added freetype-dev to make fontconfig work
# added libpng-dev to make theora work
```


```sh
# putting docker-images directory back to its original state
cd docker-images
rm -rf *
tar -xvf /Users/jds/workspace/ffmpeg-tmp/ffmpeg/docker-images/docker-images.tar
```

## Building up the alpine release ( from my desktop ) using update.py

```sh
$ ./update.py; docker build --no-cache --platform linux/amd64 -t ffmpeg-5.1-alpine320-desktop-build docker-images/5.1/alpine320
$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-7.1-scratch320-desktop-build docker-images/7.1/scratch320
$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-6.1-scratch320-desktop-build docker-images/6.1/scratch320

$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-7.1-ubuntu2404-desktop-build docker-images/7.1/ubuntu2404
$ ./update.py; time docker build --no-cache --platform linux/amd64 -t ffmpeg-7.1-ubuntu2404-edge-desktop-build docker-images/7.1/ubuntu2404-edge

```

| Image Name | Size | Build Time | Notes |
|---| ---| --- | --- | 
| ffmpeg-5.1-alpine320-desktop-build| 198 megs | 27 mins | lib
| ffmpeg-7.1-alpine320-desktop-build| 85 megs | 29 mins |


## Investigating by-hand the ubuntu image
```
docker run -it --rm --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest
```

Debugging initial ffmpeg make

## Building up the alpine image by hand

```sh
docker run -it --rm alpine:3.20 sh
# if you need to re-attach to a the running container ( I somehoe froze my terminal )
docker exec -it <container_id> sh

# take out the no-cache
apk add --update libgcc libstdc++ ca-certificates openssl zeromq libgomp expat git
buildDeps="autoconf \
                   automake \
                   bash \
                   binutils \
                   bzip2 \
                   cmake \
                   coreutils \
                   curl \
                   diffutils \
                   expat-dev \
                   file \
                   g++ \
                   gcc \
                   gperf \
                   libtool \
                   make \
                   nasm \
                   openssl-dev \
                   python3 \
                   tar \
                   xcb-proto \
                   yasm \
                   zlib-dev \
                   zeromq-dev \
                   alpine-sdk \
                   linux-headers" && \
        apk add --update ${buildDeps}
```
# Now if the packages are order independant then we can build them in any order.

```sh
# Fontconfig failed
## fontconfig https://www.freedesktop.org/wiki/Software/fontconfig/
export DIR=/tmp/fontconfig
export FONTCONFIG_VERSION=2.12.4
export PREFIX="/opt/ffmpeg"
mkdir -p ${DIR}; cd ${DIR}
curl -sLO https://www.freedesktop.org/software/fontconfig/release/fontconfig-${FONTCONFIG_VERSION}.tar.bz2
tar -jx --strip-components=1 -f fontconfig-${FONTCONFIG_VERSION}.tar.bz2
./configure --prefix="${PREFIX}" --disable-static --enable-shared
# configure: error: Package requirements (freetype2) were not met: 
# apk update
# apk search freetype2
# freetype-dev-2.13.2-r0
# apk add freetype-dev
./configure --prefix="${PREFIX}" --disable-static --enable-shared
make
make install
```

```sh
## opencore-amr https://sourceforge.net/projects/opencore-amr/
export DIR=/tmp/opencore-amr; export OPENCOREAMR_VERSION=0.1.6; export PREFIX="/opt/ffmpeg"
mkdir -p ${DIR}; cd ${DIR}
curl -sL https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-${OPENCOREAMR_VERSION}.tar.gz/download | tar -zx --strip-components=1
./configure --prefix="${PREFIX}" --enable-shared
make
make install
```

```sh
### libtheora http://www.theora.org/
#             https://stackoverflow.com/questions/4810996/how-to-resolve-configure-guessing-build-type-failure

# Dep on lib OGG
### libogg https://www.xiph.org/ogg/
export DIR=/tmp/ogg; export OGG_VERSION=1.3.2; export PREFIX="/opt/ffmpeg"
export OGG_SHA256SUM="e19ee34711d7af328cb26287f4137e70630e7261b17cbe3cd41011d73a654692 libogg-1.3.2.tar.gz"
mkdir -p ${DIR}; cd ${DIR}
curl -sLO http://downloads.xiph.org/releases/ogg/libogg-${OGG_VERSION}.tar.gz
echo ${OGG_SHA256SUM} | sha256sum --check
tar -zx --strip-components=1 -f libogg-${OGG_VERSION}.tar.gz
./configure --prefix="${PREFIX}" --enable-shared
make
make install


export DIR=/tmp/theora; export THEORA_VERSION=1.1.1; export PREFIX="/opt/ffmpeg"
export THEORA_SHA256SUM="40952956c47811928d1e7922cda3bc1f427eb75680c3c37249c91e949054916b libtheora-1.1.1.tar.gz"
mkdir -p ${DIR}; cd ${DIR}
curl -sLO http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.gz
echo ${THEORA_SHA256SUM} | sha256sum --check
tar -zx --strip-components=1 -f libtheora-${THEORA_VERSION}.tar.gz
./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared
# config.guess was really old
# Alpine uses the abuild framework for building packages, which includes autoconf.  autoconf typically installs an up-to-date version of config.guess alongside itself.
# apk verify autoconf
# apk manifest autoconf
# apk cache autoconf
# cd /; find . -name "config.guess"
# (2021-06-03) /usr/share/automake-1.16/config.guess
# (2022-01-09) /usr/share/libtool/build-aux/config.guess
# (2023-08-22) /usr/share/autoconf/build-aux/config.guess
# (2021-06-03) /usr/share/abuild/config.guess
# cp /usr/share/autoconf/build-aux/config.guess . ( no buneo )
./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared
add --target=
./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --target="linux/amd64" --enable-shared
--build=aarch64-unknown-linux-gnu
 --platform linux/amd64
# undefined reference to `png_sizeof'
make
make install 
```

docker run -it --rm --entrypoint='sh' --platform="linux/amd64" ffmpeg-7.1-alpine320-desktop-build:latest 





