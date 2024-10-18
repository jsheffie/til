FROM        ubuntu:24.04 AS base
WORKDIR     /tmp/workdir

# 149 megs
# 145 megs
RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ca-certificates openssl && \
        apt-get autoremove -y && \
        apt-get clean -y
# expat libgomp1

# ii  expat                   2.6.1-2ubuntu0.1            arm64        XML parsing C library - example application
# ii  libexpat1:arm64         2.6.1-2ubuntu0.1            arm64        XML parsing C library - runtime library
# ii  libgomp1:arm64          14.2.0-4ubuntu2~24.04       arm64        GCC OpenMP (GOMP) support library