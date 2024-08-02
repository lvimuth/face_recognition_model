from flask import Flask, request, jsonify
from face_recognition_model import recognize_face

app = Flask(__name__)

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    image_file = request.files['image']
    image_path = f"./temp/{image_file.filename}"
    image_file.save(image_path)
    
    results = recognize_face(image_path)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
