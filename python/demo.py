# Imports the Google Cloud client library

import numpy as np
from flask import Flask, request, render_template, Response, jsonify

from google.cloud import texttospeech
import base64

if __name__ == '__main__':
    # text = request.json.get('text', '')

    # Create a TextToSpeechClient
    client = texttospeech.TextToSpeechClient()

    # Configure the text-to-speech request
    synthesis_input = texttospeech.SynthesisInput(text="Test hello world")
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-F',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Generate the speech
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Convert the audio content to base64
    audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')

    # Return the audio data as a data URI in the response
    data_uri = f"data:audio/wav;base64,{audio_base64}"

    print(data_uri)
