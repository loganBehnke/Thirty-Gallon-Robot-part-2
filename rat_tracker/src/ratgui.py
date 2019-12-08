# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R.A.T._GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.roomComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.roomComboBox.setGeometry(QtCore.QRect(210, 140, 111, 31))
        self.roomComboBox.setObjectName("roomComboBox")
        self.roomComboBox.addItem("")
        self.roomComboBox.addItem("")

        self.floorComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.floorComboBox.setGeometry(QtCore.QRect(210, 100, 111, 31))
        self.floorComboBox.setObjectName("floorComboBox")
        self.floorComboBox.addItem("")
        self.floorComboBox.addItem("")
        self.floorComboBox.addItem("")

        # instantiates the "GO" button"
        self.goButton = QtWidgets.QPushButton(self.centralwidget)
        self.goButton.setGeometry(QtCore.QRect(330, 110, 75, 51))
        self.goButton.setObjectName("goButton")

        self.abortButton = QtWidgets.QPushButton(self.centralwidget)
        self.abortButton.setGeometry(QtCore.QRect(250, 500, 75, 51))
        self.abortButton.setObjectName("abortButton")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(330, 460, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.currentFloorLabel = QtWidgets.QLabel(self.centralwidget)
        self.currentFloorLabel.setGeometry(QtCore.QRect(50, 50, 331, 41))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)

        self.currentFloorLabel.setFont(font)
        self.currentFloorLabel.setObjectName("currentFloorLabel")

        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(80, 200, 421, 251))
        self.imageLabel.setObjectName("imageLabel")

        self.goingLabel = QtWidgets.QLabel(self.centralwidget)
        self.goingLabel.setGeometry(QtCore.QRect(170, 450, 151, 31))

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)

        self.goingLabel.setFont(font)
        self.goingLabel.setObjectName("goingLabel")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        pixmap = QPixmap("../res/map.jpeg")

        MainWindow.setWindowTitle(_translate("MainWindow", "R.A.T. Tracker"))
        self.roomComboBox.setItemText(0, _translate("MainWindow", "Room 101"))
        self.roomComboBox.setItemText(1, _translate("MainWindow", "Room 120"))
        self.floorComboBox.setItemText(0, _translate("MainWindow", "1st Floor"))
        self.floorComboBox.setItemText(1, _translate("MainWindow", "2nd Floor"))

        self.floorComboBox.setItemText(2, _translate("MainWindow", "3rd Floor"))

        self.floorComboBox.currentIndexChanged.connect(self.updateRoomBox)

        self.goButton.setText(_translate("MainWindow", "GO"))

        self.imageLabel.setPixmap(pixmap)

        self.goButton.clicked.connect(self.goButtonClicked)

        self.abortButton.setText(_translate("MainWindow", "ABORT"))
        self.currentFloorLabel.setText(_translate("MainWindow", "Currently on Engineering Bldg. Floor"))
        self.goingLabel.setText(_translate("MainWindow", "Going to:"))

    def goButtonClicked(self, MainWindow):
        floor = str(self.floorComboBox.currentText())
        room = str(self.roomComboBox.currentText())
        self.goingLabel.setText("Going to: " + floor + " " + room)
        self.goingLabel.repaint()

    def updateRoomBox(self, MainWindow):
        print("changed")
        _translate = QtCore.QCoreApplication.translate
        floor = str(self.floorComboBox.currentText())
        if (floor == "1st Floor"):
            self.roomComboBox.setItemText(0, _translate("MainWindow", "Room 101"))
            self.roomComboBox.setItemText(1, _translate("MainWindow", "Room 120"))
        elif (floor == "2nd Floor" ):
            self.roomComboBox.setItemText(0, _translate("MainWindow", "Room 201"))
            self.roomComboBox.setItemText(1, _translate("MainWindow", "Room 220"))
        else:
            self.roomComboBox.setItemText(0, _translate("MainWindow", "Room 301"))
            self.roomComboBox.setItemText(1, _translate("MainWindow", "Room 320"))
