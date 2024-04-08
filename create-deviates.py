#!/usr/bin/env python3
# coding: utf-8

# docker run --rm -it -v "$PWD":/usr/src/app rand-audio ./sample.py


from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import pathlib
import os
import time
import wave
import random

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

with open("data/deviates.txt", encoding="utf-8") as f:
    read_data = f.read()

# https://stackoverflow.com/questions/65949790/how-to-append-audio-frames-to-wav-file-python


chapter_size = 500
all_lines = read_data.split("\n")

# remove blank lines
while("" in all_lines):
    all_lines.remove("")

chapters = chunks(all_lines, 500)

count = 1
for lines in chapters:
    first = True

    output = wave.open(os.path.join(output_dir, "deviates" + str(count).zfill(3) + ".wav"), 'wb')

    for line in lines:
        # each line is prefaced with the line number, but since there's only 10000 lines,
        # we need to prefix with a zero to reuse the existing phrase from the main book
        line = "0" + line

        print(str(count) + " " + line)

        phrases = line.split()
        for phrase in phrases:
            if phrase == phrases[0]:
                digits = [phrase]
            else:
                digits = list(phrase)

                if digits[-1] == "-":
                    del digits[-1]
                    digits.insert(0, "-")

            for digit in digits:
                fname = digit
                if digit == ".":
                    fname = "point"
                elif digit == "-":
                    fname = "negative"
                
                filename = os.path.join(sample_dir, fname + ".wav")
                # print(filename)

                sample = wave.open(filename, 'rb')
                params = sample.getparams()
                frames = sample.readframes(sample.getnframes())

                # only do this once!
                if first:
                    output.setparams(params)
                    first = False

                output.writeframes(frames)

                sample.close()

#            print("quick break post phrase")
            pause(output, 10000)


#        print("add pause")
        pause(output, 30000)

    output.close()
    count = count + 1
