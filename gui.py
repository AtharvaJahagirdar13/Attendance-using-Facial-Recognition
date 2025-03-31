import os
import cv2
import tkinter as tk
from tkinter import messagebox, simpledialog

import self
from PIL import Image, ImageTk
import face_recognition
import sys
import subprocess
# Optionally import additional modules (e.g., db_manage, student_db_manager) if you want to log attendance
# Ensure the faces folder exists
if not os.path.exists("faces"):
    os.makedirs("faces")

class AttendanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.video_capture = cv2.VideoCapture(0)

        # Create a canvas to display the video stream
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        # Button to register unknown face
        self.btn_register = tk.Button(root, text="Register Unknown Face", command=self.register_face)
        self.btn_register.pack(pady=10)

        # Initialize lists for known face encodings and names
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

        # Start updating the video feed
        self.update_frame()

    def load_known_faces(self):
        """Load known face encodings and names from the faces folder."""
        faces_folder = "faces"
        for file in os.listdir(faces_folder):
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(faces_folder, file)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.known_face_encodings.append(encodings[0])
                    # Assumes filename format "personname_image.jpg"
                    name = file.split("_")[0]
                    self.known_face_names.append(name)

    def update_frame(self):
        """Capture a frame from the webcam and update the canvas."""
        ret, frame = self.video_capture.read()
        if ret:
            # Optionally, insert your face recognition/liveness detection logic here
            # For now, we simply display the video feed.

            # Convert frame (BGR) to RGB
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PIL image
            pil_image = Image.fromarray(cv2image)
            self.photo = ImageTk.PhotoImage(image=pil_image)
            # Display image in canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        # Schedule the next frame update
        self.root.after(10, self.update_frame)

    def register_face(self):
        """Register an unknown face."""
        ret, frame = self.video_capture.read()
        if ret:
            # Prompt the user for their name
            name = simpledialog.askstring("Register Face", "Enter your name:")
            if name:
                filename = f"{name}_image.jpg"
                save_path = os.path.join("faces", filename)
                # Save the current frame as the face image
                cv2.imwrite(save_path, frame)
                messagebox.showinfo("Registration", f"Face registered for {name}")
                # Optionally, update the known faces lists
                new_image = face_recognition.load_image_file(save_path)
                new_encodings = face_recognition.face_encodings(new_image)
                if new_encodings:
                    self.known_face_encodings.append(new_encodings[0])
                    self.known_face_names.append(name)
                else:
                    messagebox.showwarning("Registration", "No face found in the image. Please try again.")
            else:
                messagebox.showwarning("Registration", "Registration cancelled; no name entered.")

    def back_to_home(self):
        """Close this window and open home.py."""
        self.root.destroy()
        subprocess.run([sys.executable, "home.py"])

    def __del__(self):
        if self.video_capture.isOpened():
            self.video_capture.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceGUI(root)
    root.mainloop()

self.btn_register.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
self.btn_home.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

