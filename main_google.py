import cv2
import mediapipe as mp
import os

# Initialize MediaPipe face detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

# Initialize MediaPipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=100, refine_landmarks=True, min_detection_confidence=0.5)

# Create a dictionary to map names to labels
label_dict = {}
label_count = 0

# Iterate through the dataset directory
dataset_dir = 'dataset'
for name in os.listdir(dataset_dir):
    person_dir = os.path.join(dataset_dir, name)
    if os.path.isdir(person_dir):
        label_dict[name] = label_count  # Assign a unique label for each person
        label_count += 1

# Open the default camera
cap = cv2.VideoCapture(0)

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
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1)
            )

    # Display the resulting frame
    cv2.imshow('Face Mesh', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()