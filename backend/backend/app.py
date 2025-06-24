from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np
import io
from string import Template
from ultralytics import YOLO

import google.generativeai as genai

# Set your Gemini API key here
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyBbmAt0HNXKtaY7x0o6CauGJ1Uup2ydmag') # Replace with your actual default or remove if always from env
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)
CORS(app)

model = YOLO("assets/best.pt")

def inference(image):
    results = model(image)
    map_dict = results[0].names
    label = map_dict[results[0].probs.top1]
    return label

@app.route('/')
def home():
    return "Welcome to the Crop Disease Detection API!"

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)
        label = inference(img)

        first_query = Template("""
            You are a Rice Nutrient Deficiency Expert.

            Deficiency Detected: $name

            - Describe the visual symptoms associated with this deficiency.
            - Explain how this deficiency affects the overall health and growth of rice crops.
            - Provide recommendations or strategies for addressing and correcting this specific deficiency, which can help improve crop health and productivity.
        """)
        
        prompt = first_query.substitute(name=label)

        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        response = gemini_model.generate_content(prompt)

        info = response.text

        # Return label and AI response
        return jsonify({'prediction': label, 'info': info})

    return jsonify({'error': 'Failed to process the image'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        chat_response = gemini_model.generate_content(user_message)
        return jsonify({'response': chat_response.text})
    except Exception as e:
        print(f"Error during chat generation: {e}")
        return jsonify({'error': 'Failed to generate chat response'}), 500

if __name__ == '__main__':
    app.run(debug=True)
