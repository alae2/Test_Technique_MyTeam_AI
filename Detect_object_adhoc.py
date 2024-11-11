import os
import requests
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Function to download the model file 
def download_model(model_url, model_path):
    if not os.path.exists(model_path):
        print("Downloading model...")
        response = requests.get(model_url)
        if response.status_code == 200:
            with open(model_path, 'wb') as file:
                file.write(response.content)
            print("Model downloaded successfully.")
        else:
            print(f"Failed to download model, status code: {response.status_code}")
            exit()

# Download the efficientdet.tflite model if it's not already present
model_url = 'https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/int8/1/efficientdet_lite0.tflite'
model_path = 'efficientdet.tflite'
download_model(model_url, model_path)

# Initialize the MediaPipe Object Detector
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.3)
detector = vision.ObjectDetector.create_from_options(options)

# Visualization function for MediaPipe detections
def visualize(frame, detection_result):
    # Draw bounding boxes on the frame with blue or red based on the score
    for detection in detection_result.detections:
        box = detection.bounding_box
        x1, y1 = int(box.origin_x), int(box.origin_y)
        x2, y2 = int(box.origin_x + box.width), int(box.origin_y + box.height)
        
        # Change color of the box: Blue if score >= 0.5, Red if less than 0.5
        color = (0, 0, 255) if detection.categories[0].score < 0.5 else (255, 0, 0)  # Blue for higher score, Red for lower
        
        # Draw rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Put text for category and score
        cv2.putText(frame, f'{detection.categories[0].category_name} ({detection.categories[0].score:.2f})',
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame

# Function to start video acquisition
def start_video():
    global is_video_running
    if not is_video_running:
        is_video_running = True
        video_loop()  # Start video loop
        start_button.config(state=tk.DISABLED)  # Disable the start button while video is running
        end_button.config(state=tk.NORMAL)     # Enable the end button
    else:
        messagebox.showinfo("Info", "Video is already running.")

# Function to stop video acquisition
def stop_video():
    global is_video_running
    if is_video_running:
        is_video_running = False
        cap.release()  # Release the video capture
        cv2.destroyAllWindows()  # Close OpenCV windows
        start_button.config(state=tk.NORMAL)  # Enable the start button
        end_button.config(state=tk.DISABLED)  # Disable the end button
    else:
        messagebox.showinfo("Info", "The video hasn't started yet.")

# Video loop function for real-time processing
def video_loop():
    if is_video_running:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Video reading error.")
            stop_video()
            return

        # Convert frame to MediaPipe Image and detect objects
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = detector.detect(mp_image)

        # Annotate the frame with the detection result
        annotated_frame = visualize(frame, detection_result)

        # Convert the frame to a format compatible with Tkinter
        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        image = ImageTk.PhotoImage(image)

        # Update the image in the GUI
        video_label.config(image=image)
        video_label.image = image

        # Recursive call for real-time display
        video_label.after(10, video_loop)

# Initialize video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    messagebox.showerror("Error", "Cannot open the camera.")
    exit()

# Create the GUI
root = tk.Tk()
root.title("Object Detection Video")

# Set the window to fullscreen
root.attributes('-fullscreen', True)
root.config(bg='black')

# Create a label to display the video
video_label = tk.Label(root)
video_label.pack(fill=tk.BOTH, expand=True)  # Make the video label fill the window

# Create a button to start the video
start_button = tk.Button(root, text="Start Video", command=start_video)
start_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create a button to stop the video
end_button = tk.Button(root, text="End Video", command=stop_video, state=tk.DISABLED)
end_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create a button to quit the program
quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack(side=tk.LEFT, padx=10, pady=10)

# Control variable for the video
is_video_running = False

# Function to handle window closing event
def on_closing():
    if is_video_running:
        stop_video()  # Stop the video before closing
    cap.release()  # Release the video capture
    cv2.destroyAllWindows()  # Close OpenCV windows
    root.quit()  # Close the Tkinter window

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI
root.mainloop()

# Release the video capture when the GUI is closed
cap.release()
cv2.destroyAllWindows()
