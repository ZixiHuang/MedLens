
import numpy as np
from flask import Flask, request, render_template, Response, jsonify
import pickle
import cv2
from python import async_demo

#Create an app object using the Flask  class. 
app = Flask(__name__, static_url_path='/static', static_folder='static')
camera = cv2.VideoCapture(0)

#Load the trained model. (Pickle file)
# model = pickle.load(open('models/model.pkl', 'rb'))

def generate_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            print("failed to grab frame")
            break
        else:
            # k = cv2.waitKey(1)
            # if k % 256 == 32:

            detector=cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('models/haarcascade_eye.xml')
            faces=detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             #Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, home function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 

#use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def home():
    return render_template('index.html')

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


    
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


#When the Python interpreter reads a source file, it first defines a few special variables. 
#For now, we care about the __name__ variable.
#If we execute our code in the main program, like in our case here, it assigns
# __main__ as the name (__name__). 
#So if we want to run our code right here, we can check if __name__ == __main__
#if so, execute it here. 
#If we import this file (module) to another file then __name__ == app (which is the name of this python file).

if __name__ == "__main__":
    app.run(debug=True)