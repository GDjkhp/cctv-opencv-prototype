import cv2
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the pre-trained face recognition model
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_data.xml')  # Replace with the path to your face data file

names = []
for name in os.listdir('dataset'):
    names.append(name)

# Open the default camera
cam_index = 0
cap = cv2.VideoCapture(0)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Recognition")

        self.video_label = QLabel()
        self.video_label.setFixedSize(1280, 960)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Recognize faces in the frame
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]  # Region of Interest (face area)
            id_, conf = face_recognizer.predict(roi_gray)  # Recognize the face

            if conf >= 30:  # Confidence threshold (adjust as needed)
                name = names[id_]  # Get the name from the list
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        # cv2.imshow('Face Recognition', frame)

        # Capture key press
        # key = cv2.waitKey(1) & 0xFF

        # Check if 'y' key is pressed to switch camera
        # if key == ord('y'):
        #     # Release current camera
        #     self.cap.release()
            
        #     # Switch camera index
        #     cam_index = 1 if cam_index == 0 else 0
            
        #     # Re-initialize camera
        #     self.cap = cv2.VideoCapture(cam_index)
        
        # Exit the loop if the 'q' key is pressed
        # elif key == ord('q'):
        #     break

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# Release the camera and close all windows
# cap.release()
# cv2.destroyAllWindows()