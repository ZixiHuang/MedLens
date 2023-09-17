
import numpy as np
from flask import Flask, request, render_template, Response, jsonify
from flask_socketio import SocketIO, emit
import pickle
import cv2
from python import async_demo
from google.cloud import texttospeech
import base64
response = []
body_condition = ["normal"]
#Create an app object using the Flask  class. 
app = Flask(__name__, static_url_path='/static', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def client_connected():
    print('Client connected')

@socketio.on('update-body-condition')
def send_updated_data(new_condition):
    body_condition .clear()
    body_condition.append(new_condition.get('text',''))
    print('Body condition updated to: ' + str(body_condition))


def notify_client_about_openai_task_ended():
    socketio.emit('openai_task_ended', {'data': 'OpenAI task finished'})

def notify_client_about_openai_task():
    socketio.emit('openai_task_started', {'data': 'OpenAI task initiated'})

def client_text_to_speech(text_to_convert):
     # Create a TextToSpeechClient
    client = texttospeech.TextToSpeechClient()

    # Configure the text-to-speech request
    synthesis_input = texttospeech.SynthesisInput(text=text_to_convert)
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
    socketio.emit('make_text_to_speech', {'data': data_uri})



#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, home function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 

#use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def home():
    return render_template('index.html', instruction_text = async_demo.instruction)

@app.route('/synthesize', methods=['POST'])
def synthesize_text_to_speech():
    text = request.json.get('text', '')

    # Create a TextToSpeechClient
    client = texttospeech.TextToSpeechClient()

    # Configure the text-to-speech request
    synthesis_input = texttospeech.SynthesisInput(text=text)
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
    return jsonify({'audio_data_uri': data_uri})

#You can use the methods argument of the route() decorator to handle different HTTP methods.
#GET: A GET message is send, and the server returns data
#POST: Used to send HTML form data to the server.
#Add Post method to the decorator to allow for form submission. 
#Redirect to /predict page with the output

# @app.route('/predict',methods=['POST'])
# def predict():

#     int_features = [float(x) for x in request.form.values()] #Convert string inputs to float.
#     features = [np.array(int_features)]  #Convert to the form [[a, b]] for input to the model
#     prediction = model.predict(features)  # features Must be in the form [[a, b]]

#     output = round(prediction[0], 2)

#     return render_template('index.html', prediction_text='Percent with heart disease is {}'.format(output))


    
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(async_demo.analyze_img(response, body_condition[0], notify_client_about_openai_task, notify_client_about_openai_task_ended, client_text_to_speech), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get-updated-response', methods=['GET'])
def get_updated_data():
    if (not response or len(response) == 0):
        return jsonify()
    data = response.copy()
    response.clear()
    return jsonify(data)

#When the Python interpreter reads a source file, it first defines a few special variables. 
#For now, we care about the __name__ variable.
#If we execute our code in the main program, like in our case here, it assigns
# __main__ as the name (__name__). 
#So if we want to run our code right here, we can check if __name__ == __main__
#if so, execute it here. 
#If we import this file (module) to another file then __name__ == app (which is the name of this python file).

if __name__ == "__main__":
    socketio.run(app, debug=True)