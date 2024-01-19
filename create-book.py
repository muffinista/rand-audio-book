#!/usr/bin/env python3
# coding: utf-8

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import pathlib
import os
import time
# from pydub import AudioSegment
import wave

sample_dir = "samples/"
output_dir = "output/"

pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

with open("data/short.txt", encoding="utf-8") as f:
    read_data = f.read()

# https://stackoverflow.com/questions/65949790/how-to-append-audio-frames-to-wav-file-python

output = wave.open(os.path.join(output_dir, "result.wav"), 'wb')
first = True

lines = read_data.split("\n")
for line in lines:
    phrases = line.split()
    for phrase in phrases:
      filename = os.path.join(sample_dir, phrase + ".wav")
      print(filename)

      sample = wave.open(filename, 'rb')
      params = sample.getparams()
      frames = sample.readframes(sample.getnframes())

      # only do this once!
      if first:
          output.setparams(params)
          first = False

      output.writeframes(frames)

      sample.close()

      print("quick break")
    print("add pause")

output.close()
