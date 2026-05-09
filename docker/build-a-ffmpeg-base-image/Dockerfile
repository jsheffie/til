FROM        ubuntu:24.04 AS base
WORKDIR     /tmp/workdir

ARG DEBIAN_FRONTEND=noninteractive
RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends curl jq python3 python3-requests less tree file vim 

RUN      buildDeps="autoconf \
                    automake \
                    cmake \
                    build-essential \
                    texinfo \
                    curl \
                    wget \
                    tar \
                    bzip2 \
                    libexpat1-dev \
                    gcc \
                    git \
                    git-core \
                    gperf \
                    libtool \
                    make \
                    meson \
                    ninja-build \
                    nasm \
                    perl \
                    pkg-config \
                    python3 \
                    yasm \
                    zlib1g-dev \
                    libfreetype6-dev \
                    libgnutls28-dev \
                    libsdl2-dev \
                    libva-dev \
                    libvdpau-dev \
                    libnuma-dev \
                    libdav1d-dev \
                    openssl \
                    libssl-dev \
                    expat \
                    libgomp1" && \
        apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ${buildDeps}



# 149 megs
# 145 megs
# RUN     apt-get -yqq update && \
#         apt-get install -yq --no-install-recommends ca-certificates openssl && \
#         apt-get autoremove -y && \
#         apt-get clean -y
# expat libgomp1

# ii  expat                   2.6.1-2ubuntu0.1            arm64        XML parsing C library - example application
# ii  libexpat1:arm64         2.6.1-2ubuntu0.1            arm64        XML parsing C library - runtime library
# ii  libgomp1:arm64          14.2.0-4ubuntu2~24.04       arm64        GCC OpenMP (GOMP) support library