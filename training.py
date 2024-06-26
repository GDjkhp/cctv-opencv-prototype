import os
import cv2
import numpy as np

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create an empty list to store face data and labels
face_data = []
labels = []

# Create a dictionary to map names to labels
label_dict = {}
label_count = 0

# Iterate through the dataset directory
dataset_dir = 'dataset'
if not os.path.exists(dataset_dir):
    print(f"Error: '{dataset_dir}' directory not found.")
    exit(1)

for name in os.listdir(dataset_dir):
    person_dir = os.path.join(dataset_dir, name)
    if os.path.isdir(person_dir):
        label_dict[name] = label_count  # Assign a unique label for each person
        label_count += 1

        # Iterate through the image files in the person's directory
        for image_file in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_file)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Warning: Failed to read image '{image_path}'")
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Add the face data and label to the lists
            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                face_data.append(roi)
                labels.append(label_dict[name])

# Check if face data and labels are available
if not face_data or not labels:
    print("Error: No face data or labels found.")
    exit(1)

# Check if the length of face data and labels are equal
if len(face_data) != len(labels):
    print("Error: The number of face data and labels are not equal.")
    exit(1)

# Create the face recognizer and train it with the face data
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(face_data, np.array(labels))

# Save the trained model to a file
face_recognizer.write('face_data.xml')
print("Face recognition model trained and saved successfully.")