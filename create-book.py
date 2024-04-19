#!/usr/bin/env python3
# coding: utf-8


from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import pathlib
import os
import time
import wave
import random
import glob

chapter_size = 50
sample_dir = "samples/"
output_dir = "output/"

# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def chunks(l, n): 
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def pause(dest, count):
    # add a little wiggle but make it even
    wiggle = random.randrange(-1000, 1000) * 2
    blank = bytearray(count + wiggle)
    output.writeframes(blank)    

pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

with open("data/digits.txt", encoding="utf-8") as f:
    read_data = f.read()

# https://stackoverflow.com/questions/65949790/how-to-append-audio-frames-to-wav-file-python


all_lines = read_data.split("\n")

# remove blank lines
while("" in all_lines):
    all_lines.remove("")

chapters = chunks(all_lines, chapter_size)


files = glob.glob(output_dir + "/*Intro*.wav")

count = len(files) + 1
index = 1

for lines in chapters:
    first = True
    dest = os.path.join(output_dir, str(count).zfill(3) + "-Chapter-" + str(index).zfill(3) + ".wav")
    count = count + 1
    index = index + 1
    
    if os.path.isfile(dest) and os.environ.get('FORCE', False) != "True" and os.path.getsize(dest) > 0:
        print("Skipping " + dest)
        continue

    print("Generating " + dest)
    
    #print(count)
    #print(lines)
    output = wave.open(dest, 'wb')

    for line in lines:
        phrases = line.split()
        for phrase in phrases:
            filename = os.path.join(sample_dir, phrase + ".wav")
            #print(filename)

            sample = wave.open(filename, 'rb')
            params = sample.getparams()
            frames = sample.readframes(sample.getnframes())

            # only do this once!
            if first:
                output.setparams(params)
                first = False

            output.writeframes(frames)

            sample.close()

            # print("quick break")
            pause(output, 10000)


        #print("add pause")
        pause(output, 30000)

    output.close()

