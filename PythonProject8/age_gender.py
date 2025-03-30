import cv2
import numpy as np
import os

# Construct absolute paths to the models in the "models" folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGE_PROTO = os.path.join(BASE_DIR, "models", "age_deploy.prototxt")
AGE_MODEL = os.path.join(BASE_DIR, "models", "age_net.caffemodel")
GENDER_PROTO = os.path.join(BASE_DIR, "models", "gender_deploy.prototxt")
GENDER_MODEL = os.path.join(BASE_DIR, "models", "gender_net.caffemodel")

# Original age labels from the pre-trained model
ORIGINAL_AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']

# Load the pre-trained networks using OpenCV's DNN module
age_net = cv2.dnn.readNetFromCaffe(AGE_PROTO, AGE_MODEL)
gender_net = cv2.dnn.readNetFromCaffe(GENDER_PROTO, GENDER_MODEL)

def map_age_bucket(predicted_age):
    """
    Maps the original predicted age bucket to a custom range:
    - Buckets for younger ages are mapped to "17-21".
    - Buckets for older ages are mapped to "40-50".
    """
    mapping = {
        "(0-2)": "17-21",
        "(4-6)": "17-21",
        "(8-12)": "17-21",
        "(15-20)": "17-21",
        "(25-32)": "17-21",
        "(38-43)": "40-50",
        "(48-53)": "40-50",
        "(60-100)": "40-50"
    }
    return mapping.get(predicted_age, "N/A")

def predict_age_gender(face_img):
    """
    Given a face image (in BGR format), returns the predicted age range (after mapping)
    and gender. The face image is resized to 227x227 as expected by these models.
    """
    blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227),
                                 (78.4263377603, 87.7689143744, 114.895847746),
                                 swapRB=False)
    # Predict gender
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = GENDER_LIST[gender_preds[0].argmax()]

    # Predict age using the original labels
    age_net.setInput(blob)
    age_preds = age_net.forward()
    original_age = ORIGINAL_AGE_LIST[age_preds[0].argmax()]
    age = map_age_bucket(original_age)

    return age, gender
