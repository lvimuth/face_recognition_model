import face_recognition
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("path_to_your_firebase_adminsdk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def load_and_encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    return encoding

known_face_encodings = []
known_face_names = []

# Fetch known faces from Firebase
faces_ref = db.collection('faces')
for doc in faces_ref.stream():
    known_face_encodings.append(np.array(doc.to_dict()['encoding']))
    known_face_names.append(doc.id)

def recognize_face(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    results = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        results.append({"name": name})
    
    return results
