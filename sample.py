#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
"""
Speech synthesis samples for the Microsoft Cognitive Services Speech SDK
"""
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-text-to-speech-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = os.environ['AZURE_SPEECH_KEY'], os.environ['AZURE_SPEECH_REGION']

def speech_synthesis_with_voice():
    """performs speech synthesis to the default speaker with specified voice"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Sets the synthesis voice name.
    # e.g. "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)".
    # The full list of supported voices can be found here:
    # https://aka.ms/csspeech/voicenames
    # And, you can try get_voices_async method to get all available voices.
    # See speech_synthesis_get_available_voices() sample below.
    voice = "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"
    speech_config.speech_synthesis_voice_name = voice
    # Creates a speech synthesizer for the specified voice,
    # using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Receives a text from console input and synthesizes it to speaker.
    while True:
        print("Enter some text that you want to speak, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}] with voice [{}]".format(text, voice))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_using_custom_voice():
    """performs speech synthesis to the default speaker using custom voice.
       see https://aka.ms/customvoice"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Replace with the endpoint id of your Custom Voice model.
    speech_config.endpoint_id = "YourEndpointId"
    # Replace with the voice name of your Custom Voice model.
    speech_config.speech_synthesis_voice_name = "YourVoiceName"
    # Creates a speech synthesizer for Custom Voice,
    # using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Receives a text from console input and synthesizes it to speaker.
    while True:
        print("Enter some text that you want to speak, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_to_wave_file():
    """performs speech synthesis to a wave file"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Receives a text from console input and synthesizes it to wave file.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_to_mp3_file():
    """performs speech synthesis to a mp3 file"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Sets the synthesis output format.
    # The full list of supported format can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_name = "outputaudio.mp3"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Receives a text from console input and synthesizes it to mp3 file.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        # result = speech_synthesizer.speak_text_async(text).get()
        ssml = "<speak version='1.0' xml:lang='en-US' xmlns='http://www.w3.org/2001/10/synthesis' " \
           "xmlns:mstts='http://www.w3.org/2001/mstts'>" \
           "<voice name='Microsoft Server Speech Text to Speech Voice (en-US, AriaNeural)'>" \
           "0 <break strength=\"x-weak\" /> 2 <break strength=\"x-weak\" /> 3 <break strength=\"x-weak\" /> 4 <break strength=\"x-weak\" />" \
           "</voice></speak>"
        #    "<bookmark mark='bookmark_one'/> one. " \
        #    "<bookmark mark='bookmark_two'/> two. three. four.</voice></speak> "

        result = speech_synthesizer.speak_ssml_async(ssml).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_to_result():
    """performs speech synthesis and gets synthesized audio data from result."""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Receives a text from console input and synthesizes it to result.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_to_audio_data_stream():
    """performs speech synthesis and gets the audio data from single request based stream."""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Receives a text from console input and synthesizes it to result.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
            audio_data_stream = speechsdk.AudioDataStream(result)

            # You can save all the data in the audio data stream to a file
            file_name = "outputaudio.wav"
            audio_data_stream.save_to_wav_file(file_name)
            print("Audio data for text [{}] was saved to [{}]".format(text, file_name))

            # You can also read data from audio data stream and process it in memory
            # Reset the stream position to the beginning since saving to file puts the position to end.
            audio_data_stream.position = 0

            # Reads data from the stream
            audio_buffer = bytes(16000)
            total_size = 0
            filled_size = audio_data_stream.read_data(audio_buffer)
            while filled_size > 0:
                print("{} bytes received.".format(filled_size))
                total_size += filled_size
                filled_size = audio_data_stream.read_data(audio_buffer)
            print("Totally {} bytes received for text [{}].".format(total_size, text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_events():
    """performs speech synthesis and shows the speech synthesis events."""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Subscribes to events
    speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
    speech_synthesizer.synthesizing.connect(
        lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))
    speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))

    # Receives a text from console input and synthesizes it to result.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_word_boundary_event():
    """performs speech synthesis and shows the word boundary event."""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Subscribes to word boundary event
    # The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
    speech_synthesizer.synthesis_word_boundary.connect(lambda evt: print(
        "Word boundary event received: {}, audio offset in ms: {}ms".format(evt, evt.audio_offset / 10000)))

    # Receives a text from console input and synthesizes it to result.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


speech_synthesis_to_mp3_file()