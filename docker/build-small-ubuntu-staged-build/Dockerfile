# Stage 1: Build
# 486 megs
FROM ubuntu:24.04 AS builder
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y build-essential 
RUN apt-get update && apt-get install -y build-essential gcc g++ make autoconf automake libtool
RUN make

# # Stage 2: Final Image
# 100 megs
FROM ubuntu:24.04
COPY --from=builder /app /app
CMD ["/app/hello"]
