from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'my_model.h5'

# Load your trained model
model = load_model(MODEL_PATH) 
print('Model loaded. Start serving...')


# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(weights='imagenet')
# print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(50, 50))  # target_size must agree with what the trained model expects!!

    # Preprocessing the image
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)
    pred = np.argmax(preds, axis=1)
    return pred


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, '/Users/pratikmehkarkar/MS in CS/Sem-4/Deep Learning/MaleriaDetection-FinalProject/malariadetection-main/uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        pred = model_predict(file_path, model)
        os.remove(file_path)  # removes file from the server after prediction has been returned

        # Arrange the correct return according to the model. 
        # In this model 1 is Pneumonia and 0 is Normal.
        str1 = 'Malaria Parasitized (Patient has Malaria)'
        str2 = 'Uninfected (Patient does not have Malaria)'
        if pred[0] == 0:
            return str1
        else:
            return str2
    return None

    # this section is used by gunicorn to serve the app on Heroku


if __name__ == '__main__':
    app.run()
