from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Using QLabel instead of QWidget to display video
        self.camera_0 = QtWidgets.QLabel(self.centralwidget)
        self.camera_0.setGeometry(QtCore.QRect(0, 0, 320, 240))
        self.camera_0.setObjectName("camera_0")
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(50, 240, 201, 31))
        self.label_0.setAlignment(QtCore.Qt.AlignCenter)
        self.label_0.setObjectName("label_0")
        
        self.camera_1 = QtWidgets.QLabel(self.centralwidget)
        self.camera_1.setGeometry(QtCore.QRect(470, 0, 320, 240))
        self.camera_1.setObjectName("camera_1")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(540, 240, 201, 31))
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        
        self.camera_2 = QtWidgets.QLabel(self.centralwidget)
        self.camera_2.setGeometry(QtCore.QRect(0, 270, 320, 240))
        self.camera_2.setObjectName("camera_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 510, 201, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        
        self.camera_3 = QtWidgets.QLabel(self.centralwidget)
        self.camera_3.setGeometry(QtCore.QRect(470, 270, 320, 240))
        self.camera_3.setObjectName("camera_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(540, 510, 201, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_0.setText(_translate("MainWindow", "CAM_0"))
        self.label_1.setText(_translate("MainWindow", "CAM_1"))
        self.label_2.setText(_translate("MainWindow", "CAM_2"))
        self.label_3.setText(_translate("MainWindow", "CAM_3"))
