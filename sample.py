#!/usr/bin/env python3
# coding: utf-8

import azure.cognitiveservices.speech as speechsdk
import time
import os
import pathlib
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


output_dir = "samples/"
voice = "DavisNeural"

# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = os.environ['AZURE_SPEECH_KEY'], os.environ['AZURE_SPEECH_REGION']

# Creates an instance of a speech config with specified subscription key
# and service region.

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=service_region)

# Sets the synthesis output format.
# The full list of supported format can be found here:
# https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
# speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)
speech_config.speech_synthesis_voice_name = "en-US-" + voice


def speech_synthesis_to_file(ssml, file_name):
    """performs speech synthesis to a mp3 file"""
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config)

    result = speech_synthesizer.speak_ssml_async(ssml).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(
            "Speech synthesized for text [{}], and the audio was saved to [{}]".format(
                ssml,
                file_name))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(
            "Speech synthesis canceled: {}".format(
                cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(
                "Error details: {}".format(
                    cancellation_details.error_details))


def to_ssml(str):
    output = ""
    letters = list(str)
    for idx, letter in enumerate(letters):
        output += letter
        if idx < len(letters) - 1:
            output += " <break strength=\"x-weak\" /> "
    output = "<speak version='1.0' xml:lang='en-US' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'>" \
        "<voice name='Microsoft Server Speech Text to Speech Voice (en-US, " + voice + ")'>" + output + \
        "</voice></speak>"

    return output


pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

with open("data/digits.txt", encoding="utf-8") as f:
    read_data = f.read()

# get the unique set of phrases
phrases = list(set(read_data.split()))
phrases.sort()

for phrase in phrases:
    filename = os.path.join(output_dir, phrase + ".wav")
    if os.path.isfile(filename) and os.environ.get(
            'FORCE', False) != "True" and os.path.getsize(filename) > 0:
        print("Skipping " + filename)
        continue

    ssml = to_ssml(phrase)

    print(filename)
    print(ssml)

    speech_synthesis_to_file(ssml, filename)
    time.sleep(2)

# docker build -t rand-audio -f Dockerfile .
# docker run --rm -it -v "$PWD":/usr/src/app rand-audio bash
