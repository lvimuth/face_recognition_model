import firebase_admin
from firebase_admin import credentials, firestore
import face_recognition
import numpy as np

cred = credentials.Certificate("path_to_your_firebase_adminsdk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def load_and_encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    return encoding

def add_face_encoding(name, encoding):
    doc_ref = db.collection('faces').document(name)
    doc_ref.set({'encoding': encoding.tolist()})

# Example usage
image_path = "path_to_image.jpg"
name = "Person Name "
encoding = load_and_encode_image(image_path)
add_face_encoding(name, encoding)
