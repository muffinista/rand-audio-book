#!/usr/bin/env bash

mkdir -p /mnt/audiotopia/rand-audio-final
rm -rf /mnt/audiotopia/rand-audio-final/

cp data/00*Intro*.wav /mnt/audiotopia/rand-audio-output/

./generate.sh

docker run \
       -v $(pwd)/assets:/assets \
       -v "/mnt/audiotopia/rand-audio-output":/wav \
       -v "/mnt/audiotopia/rand-audio-final":/mp3 jrottenberg/ffmpeg:latest \
       -i /wav/chapter001.wav \
       -i /assets/numbers.jpg \
       -vn \
       -ar 44100 \
       -ac 1 \
       -b:a 64k \
       -id3v2_version 3 \
       -metadata:s:v title="Album cover" \
       -metadata:s:v comment="Cover (front)" \
       -metadata title="A Million Random Digits with 100,000 Normal Deviates" \
       -metadata artist="RAND Corporation" \
       -metadata album="A Million Random Digits with 100,000 Normal Deviates" \
       -metadata date="1955" \
       /mp3/test.mp3
