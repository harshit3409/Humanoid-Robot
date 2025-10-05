import cv2

from picamera2 import Picamera2

from ultralytics import YOLO

import speech_recognition as sr

import pyttsx3

import google.generativeai as genai

# Set up the camera with Picamera2

picam2 = Picamera2()

picam2.preview_configuration.main.size = (1280, 1280)

picam2.preview_configuration.main.format = "RGB888"

picam2.preview_configuration.align()

picam2.configure("preview")

picam2.start()

# Load YOLOv8 model

model = YOLO("yolov8n.pt")

# Configure Google Gemini (replace with your actual API key and model name)

genai.configure(api_key="YOUR_API_KEY")

gemini_model = genai.GenerativeModel('gemini-model-name')  # Replace with correct model name, e.g., 'gemini-pro'

# Initialize text-to-speech engine

engine = pyttsx3.init()

# Set up speech recognition

recognizer = sr.Recognizer()

microphone = sr.Microphone()

# Global variable to store the latest detected object labels

latest_detected_labels = []

# Callback function for speech recognition

def callback(recognizer, audio):

    try:

        # Recognize speech using Google Speech Recognition

        text = recognizer.recognize_google(audio)

        if text.lower() == "what is this can you explain it to me":

            if latest_detected_labels:

                # Use the first detected object

                label = latest_detected_labels[0]

                prompt = f"Explain what a {label} is."

                # Generate response from Google Gemini

                response = gemini_model.generate_content(prompt)

                explanation = response.text

                # Speak the explanation

                engine.say(explanation)

                engine.runAndWait()

            else:

                # No objects detected

                engine.say("No objects detected.")

                engine.runAndWait()

    except sr.UnknownValueError:

        print("Could not understand audio")

    except sr.RequestError as e:

        print(f"Could not request results; {e}")

# Start background listening for speech

with microphone as source:

    recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise

stop_listening = recognizer.listen_in_background(microphone, callback)

# Main loop

while True:

    # Capture a frame from the camera

    frame = picam2.capture_array()

    

    # Run YOLO model on the frame

    results = model(frame)

    

    # Extract detected object labels

    if results[0].boxes:

        detected_labels = [results[0].names[int(cls)] for cls in results[0].boxes.cls]

    else:

        detected_labels = []

    latest_detected_labels = detected_labels  # Update global variable

    

    # Annotate the frame with detection results

    annotated_frame = results[0].plot()

    

    # Calculate and display FPS

    inference_time = results[0].speed['inference']

    fps = 1000 / inference_time

    text = f'FPS: {fps:.1f}'

    

    # Define font and text position

    font = cv2.FONT_HERSHEY_SIMPLEX

    text_size = cv2.getTextSize(text, font, 1, 2)[0]

    text_x = annotated_frame.shape[1] - text_size[0] - 10  # 10 pixels from right

    text_y = text_size[1] + 10  # 10 pixels from top

    

    # Draw FPS text on the frame

    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    

    # Display the annotated frame

    cv2.imshow("Camera", annotated_frame)

    

    # Exit if 'q' is pressed

    if cv2.waitKey(1) == ord("q"):

        break

# Cleanup

stop_listening(wait_for_stop=False)

picam2.stop()

cv2.destroyAllWindows()