import os
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from liveness import eye_aspect_ratio         # Blink detection helper
from age_gender import predict_age_gender       # Age and gender prediction helper
from db_manage import DBManager                # Attendance records manager
from student_db_manager import StudentDBManager # Student details manager

# Set an eye aspect ratio threshold to detect a blink (for liveness detection)
EYE_AR_THRESH = 0.25
# --- Load All Known Faces ---
known_face_encodings = []
known_face_names = []
faces_folder = "faces"

# Loop over image files in the faces folder
for file in os.listdir(faces_folder):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(faces_folder, file)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            # Assumes filename format "personname_image.jpg"
            name = file.split("_")[0]
            known_face_names.append(name)
        else:
            print(f"Face not found in {file}")

# Make a copy of the known names to track if a student has been marked present
students = known_face_names.copy()

# --- Initialize Database Managers ---
db = DBManager(host="localhost", user="root", passwd="Anj@130206", db="attendance_db")
student_db = StudentDBManager(host="localhost", user="root", passwd="Anj@130206", db="attendance_db")

# Initialize video capture from the default webcam
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

    # Detect face locations and face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    # Get facial landmarks for liveness detection
    landmarks_list = face_recognition.face_landmarks(rgb_small_frame)

    # Loop over each detected face
    for i, ((top, right, bottom, left), face_encoding) in enumerate(zip(face_locations, face_encodings)):
        # Scale face coordinates back to the original frame size
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

        # Only proceed if the face is recognized
        if name in known_face_names:
            # Initialize blink status for the recognized face if not set
            if name not in blink_status:
                blink_status[name] = False

            # Liveness detection using blink check
            if i < len(landmarks_list):
                landmarks = landmarks_list[i]
                left_eye = landmarks.get('left_eye', [])
                right_eye = landmarks.get('right_eye', [])
                if left_eye and right_eye:
                    left_ear = eye_aspect_ratio(left_eye)
                    right_ear = eye_aspect_ratio(right_eye)
                    ear = (left_ear + right_ear) / 2.0
                    if ear < EYE_AR_THRESH:
                        blink_status[name] = True

            # If blink (liveness) is confirmed, mark attendance and update student details
            if blink_status[name]:
                cv2.putText(frame, name + " present", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
                if name in students:
                    students.remove(name)
                    # Get current date and time strings
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    time_str = datetime.now().strftime("%H:%M:%S")
                    # Insert attendance record into the attendance table
                    db.insert_attendance(name, date_str, time_str)
                    # Extract the face region of interest (ROI) from the original frame
                    face_roi = frame[top:bottom, left:right]
                    if face_roi.size != 0:
                        age, gender = predict_age_gender(face_roi)
                    else:
                        age, gender = "N/A", "N/A"
                    # Insert or update student details (age, gender) in the student_details table
                    student_db.insert_or_update_student(name, age, gender)

    # Display the resulting video frame
    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyWindow()
db.close()
student_db.close()
