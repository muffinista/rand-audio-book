#!/usr/bin/env bash

docker build -t rand-audio -f Dockerfile . && \
    # docker run --rm -it \
    #        -v "$PWD":/usr/src/app \
    #        -v "/mnt/audiotopia/rand-audio-samples":/usr/src/app/samples \
    #        -v "/mnt/audiotopia/rand-audio-output":/usr/src/app/output \
    #        rand-audio ./generate-intro.py && \
    docker run --rm -it \
           -v "$PWD":/usr/src/app \
           -v "/mnt/audiotopia/rand-audio-samples":/usr/src/app/samples \
           -v "/mnt/audiotopia/rand-audio-output":/usr/src/app/output \
           -v "/mnt/audiotopia/rand-audio-final":/usr/src/app/mp3 \
           rand-audio ./create-book.py && \
    docker run --rm -it \
           -v "$PWD":/usr/src/app \
           -v "/mnt/audiotopia/rand-audio-samples":/usr/src/app/samples \
           -v "/mnt/audiotopia/rand-audio-output":/usr/src/app/output \
           -v "/mnt/audiotopia/rand-audio-final":/usr/src/app/mp3 \
           rand-audio ./create-deviates.py
