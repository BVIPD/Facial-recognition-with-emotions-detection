# -*- coding: utf-8 -*-
"""Emotions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LPTD7DS8Q9WuAbc6zdqmY-xz6BaifU6Z
"""

!pip install deepface

!pip install face_recognition

from google.colab import files
import cv2
from deepface import DeepFace
from matplotlib import pyplot as plt

# Upload an image
uploaded = files.upload()
image_path = next(iter(uploaded))

# Read the uploaded image
image = cv2.imread(image_path)

# Detect faces and analyze emotions
try:
    analysis = DeepFace.analyze(image, actions=['emotion'])

    # Check if the result is a list (multiple faces detected)
    if isinstance(analysis, list):
        for idx, face_analysis in enumerate(analysis):
            emotion = face_analysis['dominant_emotion']
            print(f"Detected emotion for face {idx + 1}: {emotion}")
    else:
        # Single face detected
        emotion = analysis['dominant_emotion']
        print("Detected emotion:", emotion)

    # Display the image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.title(f"Emotion(s) detected")
    plt.show()

except Exception as e:
    print(f"Error processing image for emotion: {e}")

pip install opencv-python-headless deepface

import os
from IPython.display import display, Javascript

# Define the folder path where you want to save the image
folder_path = '/content/my_images'  # You can change the folder name and path
os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

# Function to capture image and save it to a specific folder
def take_photo(filename='photo.jpg'):
    js = Javascript(f'''
        async function takePhoto() {{
            const div = document.createElement('div');
            const video = document.createElement('video');
            video.style.display = 'block';
            const stream = await navigator.mediaDevices.getUserMedia({{video: true}});
            document.body.appendChild(div);
            div.appendChild(video);
            video.srcObject = stream;
            await video.play();

            // Create a button to capture the image
            const button = document.createElement('button');
            button.innerText = 'Capture Photo';
            div.appendChild(button);

            // Wait for button click
            await new Promise((resolve) => button.onclick = resolve);
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getTracks().forEach(track => track.stop());
            div.remove();

            // Convert the image to base64 and send it to Python
            const imgData = canvas.toDataURL('image/jpeg').split(',')[1];
            google.colab.kernel.invokeFunction('notebook.save_image', [imgData, '{folder_path}/{filename}'], {{}})
        }}
        takePhoto();
    ''')
    display(js)

# Register a callback function to handle the base64 image data sent from JavaScript
import base64

def save_image(data, filename):
    if filename is None:
        print("Error: No filename provided.")
        return

    try:
        # Save the image to the specified folder
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(data))
        print(f"Image saved as {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")

# Register the save_image function with Google Colab
from google.colab import output
output.register_callback('notebook.save_image', save_image)

# Call the function to take a photo
take_photo()

import cv2
from deepface import DeepFace
from matplotlib import pyplot as plt
import os

# Check if the image exists in the folder
image_path = '/content/my_images/photo.jpg'
if os.path.exists(image_path):
    print(f"Image found at: {image_path}")

    # Load the saved image
    image = cv2.imread(image_path)

    # Run emotion analysis on the image
    try:
        # DeepFace analyzes the image for emotions
        analysis = DeepFace.analyze(image, actions=['emotion'])

        # Since the analysis result is a list of dictionaries, you need to extract the first item
        emotion = analysis[0]['dominant_emotion']
        print("Detected emotion:", emotion)

        # Display the image with the detected emotion
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
        plt.axis('off')
        plt.title(f"Detected Emotion: {emotion}")
        plt.show()

    except Exception as e:
        print(f"Error processing image for emotion: {e}")
else:
    print("Image not found. Please capture the photo again.")