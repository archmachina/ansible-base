FROM python:3.11.4-bullseye

ARG DEBIAN_FRONTEND=noninteractive

# Install any OS packages
RUN apt-get update && apt-get install -yq --no-install-recommends sshpass && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 -r ansible && \
  useradd -u 1000 -g 1000 -d /work ansible && \
  mkdir /work && \
  chmod 775 /work && \
  chown ansible:ansible /work

WORKDIR /work
ENV HOME /work

COPY scripts/* /usr/local/bin/
COPY --chown=1000:1000 "./requirements.txt" "./requirements.yml" /work

ARG BUILD_VERSION
RUN echo "$BUILD_VERSION" > /version.txt && \
  chown ansible:ansible /version.txt

USER 1000:1000

ENTRYPOINT [ "/usr/local/bin/entrypoint" ]

