#!/usr/bin/env python3
# coding: utf-8

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import pathlib
import os
import time
from pydub import AudioSegment

sample_dir = "samples/"
output_dir = "output/"

pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

with open("data/short.txt", encoding="utf-8") as f:
    read_data = f.read()

output = None

lines = read_data.split("\n")
for line in lines:
    phrases = line.split()
    for phrase in phrases:
      filename = os.path.join(sample_dir, phrase + ".wav")
      print(filename)
      s = AudioSegment.from_wav(filename)
      if output is None:
         output = s
      else:
        output += s
      print("quick break")
    print("add pause")

output.export(os.path.join(output_dir, "result.wav"), format="wav")