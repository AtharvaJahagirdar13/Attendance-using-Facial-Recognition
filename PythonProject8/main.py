import os
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from liveness import eye_aspect_ratio  # Import our liveness detection function
from db_manage import DBManager  # Import our database manager

# Set an eye aspect ratio threshold to detect a blink
EYE_AR_THRESH = 0.25

# --- Load All Known Faces ---
known_face_encodings = []
known_face_names = []
faces_folder = "faces"

for file in os.listdir(faces_folder):
    if file.endswith(".jpg") or file.endswith(".png"):
        image_path = os.path.join(faces_folder, file)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            # Extract the person's name from the file name (expects "personname_image.jpg")
            name = file.split("_")[0]
            known_face_names.append(name)
        else:
            print(f"Face not found in {file}")

students = known_face_names.copy()

# --- Initialize Database Manager ---
db = DBManager(host="localhost", user="root", passwd="Anj@130206", db="attendance_db")

# Initialize Video Capture
video_capture = cv2.VideoCapture(0)

# Dictionary to keep track of blink (liveness) status for each recognized face
blink_status = {}

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Resize frame for faster processing and convert to RGB
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and encodings on the reduced frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Get facial landmarks for liveness detection
    landmarks_list = face_recognition.face_landmarks(rgb_small_frame)

    # Loop over each detected face
    for i, ((top, right, bottom, left), face_encoding) in enumerate(zip(face_locations, face_encodings)):
        # Scale back up the face locations since the frame was resized
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a bounding box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Perform face recognition
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        else:
            name = "Unknown"

        # Only process further if the face is recognized
        if name in known_face_names:
            # Initialize blink status for the person if not already set
            if name not in blink_status:
                blink_status[name] = False

            # Liveness detection using blink check:
            if i < len(landmarks_list):
                landmarks = landmarks_list[i]
                left_eye = landmarks.get('left_eye', [])
                right_eye = landmarks.get('right_eye', [])
                if left_eye and right_eye:
                    left_ear = eye_aspect_ratio(left_eye)
                    right_ear = eye_aspect_ratio(right_eye)
                    ear = (left_ear + right_ear) / 2.0

                    # If the EAR is below the threshold, consider it a blink
                    if ear < EYE_AR_THRESH:
                        blink_status[name] = True

            # Log attendance only if liveness (blink) is confirmed
            if blink_status[name]:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (255, 0, 0)
                thickness = 3
                lineType = 2
                cv2.putText(frame, name + " present", bottomLeftCornerOfText, font,
                            fontScale, fontColor, thickness, lineType)
                if name in students:
                    students.remove(name)
                    # Get the current date and time
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    time_str = datetime.now().strftime("%H:%M:%S")
                    # Insert the attendance record into MySQL
                    db.insert_attendance(name, date_str, time_str)

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyWindow()

# Close database connection
db.close()
