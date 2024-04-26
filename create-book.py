#!/usr/bin/env python3
# coding: utf-8


from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import pathlib
import os
import time
import wave
import random


from shared import *


chapter_size = 50
sample_dir = "samples/"
output_dir = "output/"
assets_dir = "/usr/src/app/assets/"
intro_src_dir = "/usr/src/app/data/"
final_dir = "mp3/"

pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(final_dir).mkdir(parents=True, exist_ok=True)

def pause(count):
    # add a little wiggle but make it even
    wiggle = random.randrange(-1000, 1000) * 2
    blank = bytearray(count + wiggle)
    #dest.writeframes(blank)
    return blank

#
# Since we pre-mix this, it's hardcoded for now
#
def intro_count():
    return 5

def digit_chapter_count():
    return len(list(digit_chapters()))

def deviate_chapter_count():
    return len(list(deviate_chapters()))

def total_chapter_count():
    return intro_count() + digit_chapter_count() + deviate_chapter_count()


def digit_chapters():
    with open("data/digits.txt", encoding="utf-8") as f:
        read_data = f.read()

    all_lines = read_data.split("\n")

    # remove blank lines
    while("" in all_lines):
        all_lines.remove("")

    return chunks(all_lines, chapter_size)

def deviate_chapters():
    with open("data/deviates.txt", encoding="utf-8") as f:
        read_data = f.read()

    # https://stackoverflow.com/questions/65949790/how-to-append-audio-frames-to-wav-file-python

    all_lines = read_data.split("\n")

    # remove blank lines
    while("" in all_lines):
        all_lines.remove("")

    return chunks(all_lines, chapter_size)


def generate_intro():
    total_count = total_chapter_count()

    # 001-Intro-1.wav

    for index in range(1, intro_count() + 1):
        dest = os.path.join(intro_src_dir, str(index).zfill(3) + "-Intro-" + str(index) + ".wav")
        mp3_dest = os.path.join(final_dir, str(index).zfill(3) + "-Intro-" + str(index).zfill(3) + ".mp3")

        if os.path.isfile(mp3_dest) and os.environ.get('FORCE', False) != "True" and os.path.getsize(mp3_dest) > 0:
            print("Skipping " + mp3_dest)
        else:
            print("Generating " + mp3_dest)
            generate_mp3(dest, mp3_dest, assets_dir + "numbers-small.jpg", "Introduction: Part " + str(index), index, total_count)

        
def generate_digits():
    total_count = total_chapter_count()
    chapters = digit_chapters()

    count = intro_count() + 1
    index = 1

    for lines in chapters:
        first = True
        dest = os.path.join(output_dir, str(count).zfill(3) + "-Chapter-" + str(index).zfill(3) + ".wav")
        mp3_dest = os.path.join(final_dir, str(count).zfill(3) + "-Chapter-" + str(index).zfill(3) + ".mp3")

        if os.path.isfile(dest) and os.environ.get('FORCE', False) != "True" and os.path.getsize(dest) > 0:
            print("Skipping " + dest)
        else:
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
                    output.writeframes(pause(10000))


                # print("add pause")
                output.writeframes(pause(30000))

            output.close()


        if os.path.isfile(mp3_dest) and os.environ.get('FORCE', False) != "True" and os.path.getsize(mp3_dest) > 0:
            print("Skipping " + mp3_dest)
        else:
            print("Generating " + mp3_dest)
            generate_mp3(dest, mp3_dest, assets_dir + "numbers-small.jpg", "Digits: Chapter " + str(index), count, total_count)

        count = count + 1
        index = index + 1

def generate_deviates():
    chapters = deviate_chapters()
    total_count = total_chapter_count()

    count = intro_count() + digit_chapter_count() + 1
    index = 1

    for lines in chapters:
        first = True
        dest = os.path.join(output_dir, str(count).zfill(3) + "-Deviates-" + str(index).zfill(3) + ".wav")
        mp3_dest = os.path.join(final_dir, str(count).zfill(3) + "-Deviates-" + str(index).zfill(3) + ".mp3")

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

                    output.writeframes(pause(10000))


                output.writeframes(pause(30000))

            output.close()


        if os.path.isfile(mp3_dest) and os.environ.get('FORCE', False) != "True" and os.path.getsize(mp3_dest) > 0:
            print("Skipping " + mp3_dest)
        else:
            print("Generating " + mp3_dest)
            generate_mp3(dest, mp3_dest, assets_dir + "numbers-small.jpg", "Deviates: Chapter " + str(index), count, total_count)

        count = count + 1
        index = index + 1



generate_intro()
generate_digits()
generate_deviates()
