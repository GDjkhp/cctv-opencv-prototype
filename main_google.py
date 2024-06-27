import cv2
import mediapipe as mp
import os
# from training import *

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the pre-trained face recognition model
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_data.xml')  # Replace with the path to your face data file

# Define the names for the recognized faces
names = []
for name in os.listdir('dataset'):
    names.append(name)

# Initialize Video Capture
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(max_num_faces=10) as face_mesh:
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        results = face_mesh.process(rgb_frame)

        # Draw face mesh and landmarks on the frame
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw the face landmarks and bounding box
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1)
                )
                
                # Get bounding box from landmarks
                h, w, _ = frame.shape
                x_min = min([landmark.x for landmark in face_landmarks.landmark]) * w
                x_max = max([landmark.x for landmark in face_landmarks.landmark]) * w
                y_min = min([landmark.y for landmark in face_landmarks.landmark]) * h
                y_max = max([landmark.y for landmark in face_landmarks.landmark]) * h
                
                # Draw bounding box 
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 0, 0), 2)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Recognize faces in the frame
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]  # Region of Interest (face area)
            id_, conf = face_recognizer.predict(roi_gray)  # Recognize the face

            if conf >= 50:  # Confidence threshold (adjust as needed)
                name = names[id_]  # Get the name from the list
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()