
def build_ffmpeg_initial():
    export DIR=/tmp/ffmpeg; export FFMPEG_VERSION=7.1 
    mkdir -p ${DIR}; cd ${DIR}
    curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2
    tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2
    ./configure     --disable-debug  --disable-doc    --disable-ffplay   --enable-shared --enable-gpl  --extra-libs=-ldl
    make
    make install



def build_ffmpeg_stage2():
export DIR=/tmp/ffmpeg; export FFMPEG_VERSION=7.1; \
export MAKEFLAGS="-j2"; \
export PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"; \
export PREFIX="/opt/ffmpeg"; \
export LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"
mkdir -p ${DIR}; cd ${DIR}
curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2
    # dpkg -l |grep srt
./configure --disable-debug --disable-doc --disable-ffplay --enable-fontconfig --enable-gpl --enable-libaom \
--enable-libaribb24 --enable-libass --enable-libbluray --enable-libdav1d --enable-libfdk-aac --enable-libfreetype \
--enable-libkvazaar --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg \
--enable-libopus --enable-libsrt --enable-libsvtav1 --enable-libtheora --enable-libvidstab --enable-libvmaf \
--enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid \
--enable-libzimg --enable-libzmq --enable-nonfree --enable-openssl --enable-postproc --enable-shared \
--enable-small --enable-version3 \
--extra-cflags="-I${PREFIX}/include -I/usr/include/x86_64-linux-gnu" \
--extra-ldflags="-L${PREFIX}/lib -L/usr/lib/x86_64-linux-gnu" \
--extra-libs=-ldl --extra-libs=-lm --extra-libs=-lpthread --ld=g++ \
--prefix="${PREFIX}" | tee /root/ffmpeg_configure_output.txt

    make clean
    make 
    make install
    make tools/zmqsend && cp tools/zmqsend ${PREFIX}/bin/
    make distclean
    hash -r 
    cd tools

    make qt-faststart && cp qt-faststart ${PREFIX}/bin/

RUN \
if ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | grep -q . ; then \
    ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/; \
fi
if ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | grep -q . ; then \
    ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/; \
fi
for lib in /usr/local/lib/*.so.*; do ln -sf "${lib##*/}" "${lib%%.so.*}".so; done && \
cp ${PREFIX}/bin/* /usr/local/bin/ && \
cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ && \
LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf && \
cp -r ${PREFIX}/include/libav* ${PREFIX}/include/libpostproc ${PREFIX}/include/libsw* /usr/local/include && \
161 files
mkdir -p /usr/local/lib/pkgconfig && \
for pc in ${PREFIX}/lib/pkgconfig/libav*.pc ${PREFIX}/lib/pkgconfig/libpostproc.pc ${PREFIX}/lib/pkgconfig/kvazaar.pc ${PREFIX}/lib/pkgconfig/libsw*.pc; do \
    sed "s:${PREFIX}:/usr/local:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"; \
done

Curent image ffmpeg-7.1-ubuntu2404-desktop-build is at 266 megabytes.
maybe we can chop out the /usr/lib/x86_64-linux-gnu and /usr/lib64 


Lets finish the edge one: ffmpeg-7.1-ubuntu2404-edge-desktop-build:latest
Built it big ( so I can debug it )
Built it debug the theora build.
docker run -it --rm --entrypoint=bash --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-edge-desktop-build:latest

### libtheora http://www.theora.org/ ( xiph )
#             https://stackoverflow.com/questions/4810996/how-to-resolve-configure-guessing-build-type-failure
# RUN \
#         echo "Building libtheora-${THEORA_VERSION}" && \
#         DIR=/tmp/theora && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         curl -sLO http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.gz && \
#         echo ${THEORA_SHA256SUM} | sha256sum --check && \
#         tar -zx --strip-components=1 -f libtheora-${THEORA_VERSION}.tar.gz && \
#         cp /usr/share/misc/config.guess . && \
#         ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

export DIR=/tmp/ffmpeg; export FFMPEG_VERSION=7.1; \
export MAKEFLAGS="-j2"; \
export PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"; \
export PREFIX="/opt/ffmpeg"; \
export LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64:/usr/lib/x86_64-linux-gnu"; \
export THEORA_VERSION=1.1.1 \
export THEORA_VERSION=1.2.0alpha1 \
export THEORA_SHA256SUM="40952956c47811928d1e7922cda3bc1f427eb75680c3c37249c91e949054916b libtheora-1.1.1.tar.gz" \
export DIR=/tmp/theora \
mkdir -p ${DIR}; cd ${DIR}
curl -sLO http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.gz
          http://downloads.xiph.org/releases/theora/libtheora-1.2.0alpha1.tar.gz
echo ${THEORA_SHA256SUM} | sha256sum --check
tar -zx --strip-components=1 -f libtheora-${THEORA_VERSION}.tar.gz
# ln -s /usr/bin/sdl2-config /usr/bin/sdl-config
# ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared --disable-sdltest
./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared --disable-examples
make install

WARNING: *** doxygen not found, API documentation will not be built

docker run -it --rm --entrypoint=bash --dns=8.8.8.8 --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-edge-desktop-build:latest
git clone https://git.xiph.org/theora.git



export DIR=/tmp/ffmpeg; export FFMPEG_VERSION=7.1; \
export MAKEFLAGS="-j2"; \
export PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"; \
export PREFIX="/opt/ffmpeg"; \
export LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"
mkdir -p ${DIR}; cd ${DIR}
curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2
    # dpkg -l |grep srt
./configure --disable-debug --disable-doc --disable-ffplay --enable-fontconfig --enable-gpl --enable-libaom \
--enable-libaribb24 --enable-libass --enable-libbluray --enable-libdav1d --enable-libfdk-aac --enable-libfreetype \
--enable-libkvazaar --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg \
--enable-libopus --enable-libsrt --enable-libsvtav1 --enable-libtheora --enable-libvidstab --enable-libvmaf \
--enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid \
--enable-libzimg --enable-libzmq --enable-nonfree --enable-openssl --enable-postproc --enable-shared \
--enable-small --enable-version3 \
--extra-cflags="-I${PREFIX}/include -I/usr/include/x86_64-linux-gnu" \
--extra-ldflags="-L${PREFIX}/lib -L/usr/lib/x86_64-linux-gnu" \
--extra-libs=-ldl --extra-libs=-lm --extra-libs=-lpthread --ld=g++ \
--prefix="${PREFIX}" | tee /root/ffmpeg_configure_output.txt

    make clean
    make 
    make install
    make tools/zmqsend && cp tools/zmqsend ${PREFIX}/bin/
    make distclean
    hash -r 
    cd tools

    make qt-faststart && cp qt-faststart ${PREFIX}/bin/



        DIR=/tmp/libsvtav1 && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v${SVTAV1_VERSION}/SVT-AV1-v${SVTAV1_VERSION}.tar.gz | \
        tar -zx --strip-components=1 -f SVT-AV1-v${SVTAV1_VERSION}.tar.gz
        mkdir -p SVT-AV1/build && \
        cd SVT-AV1/build && \
        cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${PREFIX}"  -DCMAKE_BUILD_TYPE=Release -DBUILD_DEC=OFF -DBUILD_SHARED_LIBS=OFF ..; \
        make ; \
        make install ; \
        rm -rf ${DIR}

Install the project...
-- Install configuration: "Release"
-- Installing: /opt/ffmpeg/lib/libSvtAv1Enc.a
-- Installing: /opt/ffmpeg/lib/pkgconfig/SvtAv1Enc.pc
-- Installing: /opt/ffmpeg/bin/SvtAv1EncApp
-- Installing: /opt/ffmpeg/include/svt-av1
-- Installing: /opt/ffmpeg/include/svt-av1/EbSvtAv1Enc.h
-- Installing: /opt/ffmpeg/include/svt-av1/EbSvtAv1Metadata.h
-- Installing: /opt/ffmpeg/include/svt-av1/EbDebugMacros.h
-- Installing: /opt/ffmpeg/include/svt-av1/EbSvtAv1Formats.h
-- Installing: /opt/ffmpeg/include/svt-av1/EbSvtAv1.h
-- Installing: /opt/ffmpeg/include/svt-av1/EbSvtAv1ErrorCodes.h
-- Installing: /opt/ffmpeg/include/svt-av1/EbSvtAv1ExtFrameBuf.h

        git clone --depth=1 https://gitlab.com/AOMediaCodec/SVT-AV1.git
cd SVT-AV1
cd Build
cmake .. -G"Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
make -j $(nproc)
sudo make install