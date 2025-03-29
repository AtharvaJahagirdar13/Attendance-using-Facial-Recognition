import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)
atharva_image = cv2.imread("faces/atharva_image.jpg")  # OpenCV loads in BGR
atharva_image = cv2.cvtColor(atharva_image, cv2.COLOR_BGR2RGB)  # Convert to RGB


atharva_image=face_recognition.load_image_file("faces/atharva_image.jpg")
atharva_encoding=face_recognition.face_encodings(atharva_image)[0]

known_face_encodings=[atharva_encoding]
known_face_names=['atharva']

students= known_face_names.copy()

face_locations = []
face_encodings = []

now=datetime.now()
current_time = now.strftime("%H-%M-%S")


f = open(f"{current_time}.csv","w+",newline="")
lnwr=csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations=face_recognition.face_locations(rgb_small_frame)
    face_encodings=face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break