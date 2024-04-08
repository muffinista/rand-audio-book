#!/usr/bin/env python3
# coding: utf-8

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import glob
import pathlib
import os
import time
import azure.cognitiveservices.speech as speechsdk

output_dir = "samples/"
voice = "DavisNeural"

# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = os.environ['AZURE_SPEECH_KEY'], os.environ['AZURE_SPEECH_REGION']

# Creates an instance of a speech config with specified subscription key and service region.

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Sets the synthesis output format.
# The full list of supported format can be found here:
# https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
# speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)
speech_config.speech_synthesis_voice_name = "en-US-" + voice

def speech_synthesis_to_file(ssml, file_name):
    """performs speech synthesis to a mp3 file"""
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    result = speech_synthesizer.speak_ssml_async(ssml).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(ssml, file_name))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)


files = glob.glob("data/intro-*.ssml")
for fname in files:
    with open(fname, encoding="utf-8") as f:
        intro_ssml = f.read()

        filename = fname.replace(".ssml", ".wav")

        if os.path.isfile(filename) and os.environ.get('FORCE', False) != "True" and os.path.getsize(filename) > 0:
            print("Skipping " + filename)
        else:
            print(filename)
            print(intro_ssml)

            speech_synthesis_to_file(intro_ssml, filename)
            time.sleep(2)

# docker build -t rand-audio -f Dockerfile .
# docker run --rm -it -v "$PWD":/usr/src/app rand-audio bash
