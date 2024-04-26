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

from shared import *

chapter_size = 50
sample_dir = "samples/"
output_dir = "output/"
final_dir = "mp3/"

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


all_lines = read_data.split("\n")

# remove blank lines
while("" in all_lines):
    all_lines.remove("")

chapters = chunks(all_lines, 50)

intro_files = glob.glob(output_dir + "/*Intro*.wav")
chapter_files = glob.glob(output_dir + "/*Chapter*.wav")

count = len(intro_files) + len(chapter_files) + 1
index = 1


for lines in chapters:
    first = True
    dest = os.path.join(output_dir, str(count).zfill(3) + "-Deviates-" + str(index).zfill(3) + ".wav")

    
    if os.path.isfile(dest) and os.environ.get('FORCE', False) != "True" and os.path.getsize(dest) > 0:
        print("Skipping " + dest)
    else:
        print("Generating " + dest)
    
        output = wave.open(dest, 'wb')

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

                pause(output, 10000)


            pause(output, 30000)

        output.close()


    mp3_dest = os.path.join(final_dir, str(count).zfill(3) + "-Deviates-" + str(index).zfill(3) + ".mp3")
    
    if os.path.isfile(mp3_dest) and os.environ.get('FORCE', False) != "True" and os.path.getsize(mp3_dest) > 0:
        print("Skipping " + mp3_dest)
    else:
        print("Generating " + mp3_dest)
        generate_mp3(dest, mp3_dest, assets_dir + "numbers-small.jpg", "Chapter " + str(count) + " - Digits", index, 1000)

    count = count + 1
    index = index + 1
