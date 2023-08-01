FROM python:3.11.4-bullseye

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -yq --no-install-recommends sshpass && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 -r ansible && \
  useradd -u 1000 -g 1000 -d /work ansible && \
  mkdir /work && \
  chmod 755 /work && \
  chown ansible:ansible /work

WORKDIR /work
ENV HOME /work

ARG BUILD_VERSION
RUN echo "$BUILD_VERSION" > /version.txt

USER 1000:1000
