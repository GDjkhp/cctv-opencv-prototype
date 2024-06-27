import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from cameras_ui import Ui_MainWindow

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the pre-trained face recognition model
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_data.xml')  # Replace with the path to your face data file

names = []
for name in os.listdir('dataset'):
    names.append(name)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.caps = [
            cv2.VideoCapture(0),
            cv2.VideoCapture(1),
            cv2.VideoCapture(""),
            cv2.VideoCapture(""),
        ]  # Initialize video captures for 4 cameras

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)  # 30 ms for approximately 30 frames per second

    def update_frames(self):
        frames = [cap.read()[1] for cap in self.caps]
        
        if frames[0] is not None:
            self.display_frame(frames[0], self.camera_0)
        if frames[1] is not None:
            self.display_frame(frames[1], self.camera_1)
        if frames[2] is not None:
            self.display_frame(frames[2], self.camera_2)
        if frames[3] is not None:
            self.display_frame(frames[3], self.camera_3)

    def display_frame(self, frame, label):
        # Resize the image to 1/4th of the original size
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

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

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Scale the image to fit the label dimensions
        scaled_qt_image = qt_image.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(QPixmap.fromImage(scaled_qt_image))

    def closeEvent(self, event):
        for cap in self.caps:
            cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
