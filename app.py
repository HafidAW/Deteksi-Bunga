from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import streamlit as st

app = Flask(__name__)

# Path to save uploaded images
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained model
model = tf.keras.models.load_model('model/bunga_cnn_model.h5')

# Dictionary to map predicted indices to flower names
class_names = ['Male', 'Female']  # Ensure the correct order

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the image for prediction
        img = image.load_img(file_path, target_size=(150, 150))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        
        # Predict the class (for binary classification)
        prediction = model.predict(img_array)
        
        # Get class label and confidence
        if prediction[0][0] < 0.5:
            class_label = 'Male'
            confidence = round((1 - prediction[0][0]) * 100, 2)  # Confidence for Male
        else:
            class_label = 'Female'
            confidence = round(prediction[0][0] * 100, 2)  # Confidence for Female
        
        # Render the template with the result
        return render_template('index.html', file_path=filename, class_label=class_label, confidence=confidence)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
