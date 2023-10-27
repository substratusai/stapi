FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04


ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8080

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && \
    apt-get -y --no-install-recommends install python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY main.py .
COPY entrypoint.sh /usr/local/bin/
CMD [ "entrypoint.sh" ]

EXPOSE ${PORT}
