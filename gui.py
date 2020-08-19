from PyQt5.QtWidgets import (QApplication, QMainWindow, QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout,
	QLabel, QPushButton, QStyleFactory, QWidget, QFileDialog)
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import sys
import serial
import serial.tools.list_ports
import cv2
import numpy as np
import subprocess

videoX = 1260
videoY = 945

class videoThread(QThread):
	changePixmap = pyqtSignal(QImage)

	def run(self):
		cap = cv2.VideoCapture(0)

		if(cap.isOpened() == False):
			print("Error opening video stream.")
			return

		print("Camera opened")

		while(True):
			ret, frame = cap.read()
			if(ret):
				rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				h, w, ch = rgbImage.shape
				bytesPerLine = ch*w
				convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
				p = convertToQtFormat.scaled(videoX,videoY,Qt.KeepAspectRatio)
				self.changePixmap.emit(p)

class pgmThread(QThread):
	uploadComplete = pyqtSignal()

	def __init__(self, sofFile):
		QThread.__init__(self)
		self.sofFile = sofFile

	def run(self):
		subprocess.run(["quartus_pgm","-m","jtag","-o",self.sofFile])
		self.uploadComplete.emit()
		# quartus_pgm -m jtag -o "p;path/to/file.sof@2”

class GUI(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setGeometry(100,100,1700,900)
		self.setWindowTitle("McMaster University Department of Computing and Software DE1-SoC Virtual Interface")
		self.setStyleSheet("QLabel {font: 14pt Calibri}" + "QPushButton {font: 14pt Calibri}" + "QGroupBox {font: 20pt Calibri}")

		# 1 make video group
		self.__createVideo__()
		# 2 make key group
		self.__createKeys__()
		# 3 make switch group
		self.__createSwitches__()
		# 4 make file upload group 
		self.__createFileUploader__()
		# 5 make arduino/camera status group
		self.__createStatus__()

		# combine 2, 3 into an hbox
		inputs_Layout_1 = QHBoxLayout()
		inputs_Layout_1.addWidget(self.keyGroupBox)
		inputs_Layout_1.addWidget(self.switchGroupBox)
		# combine (2,3), 4, 5 into a vbox
		inputs_Layout_2 = QVBoxLayout()
		inputs_Layout_2.addWidget(self.fileUploaderGroupBox)
		inputs_Layout_2.addLayout(inputs_Layout_1)
		inputs_Layout_2.addWidget(self.statusGroupBox)
		inputs_Layout_2.addStretch(0)
		# combine ((2,3),4), 1 into an hbox
		main_Layout = QHBoxLayout()
		main_Layout.addWidget(self.videoGroupBox)
		main_Layout.addLayout(inputs_Layout_2)
		
		# create a widget, set the layout, and set the combination to the central widget
		centralWidget = QWidget()
		centralWidget.setLayout(main_Layout)
		self.setCentralWidget(centralWidget)

		self.__setupArduino__()

	def __arduinoMissing__(self):
		# update arduino device status
		self.arduinoStatus.setText("Arduino Missing")

		# deactivate check arduino button
		self.arduinoReconnectButton.setEnabled(True)

		# activate KEYs and SWs
		self.key_togglePB1.setEnabled(False)
		self.key_togglePB2.setEnabled(False)
		self.key_togglePB3.setEnabled(False)
		self.key_togglePB4.setEnabled(False)
		self.switch_togglePB1.setEnabled(False)
		self.switch_togglePB2.setEnabled(False)
		self.switch_togglePB3.setEnabled(False)
		self.switch_togglePB4.setEnabled(False)
		self.switch_togglePB5.setEnabled(False)
		self.switch_togglePB6.setEnabled(False)
		self.switch_togglePB7.setEnabled(False)
		self.switch_togglePB8.setEnabled(False)
		self.switch_togglePB9.setEnabled(False)
		self.switch_togglePB10.setEnabled(False)

	def __arduinoPresent__(self):
		# update arduino device status
		self.arduinoStatus.setText("Arduino Present")

		# deactivate check arduino button
		self.arduinoReconnectButton.setEnabled(False)

		# activate KEYs and SWs
		self.key_togglePB1.setEnabled(True)
		self.key_togglePB2.setEnabled(True)
		self.key_togglePB3.setEnabled(True)
		self.key_togglePB4.setEnabled(True)
		self.switch_togglePB1.setEnabled(True)
		self.switch_togglePB2.setEnabled(True)
		self.switch_togglePB3.setEnabled(True)
		self.switch_togglePB4.setEnabled(True)
		self.switch_togglePB5.setEnabled(True)
		self.switch_togglePB6.setEnabled(True)
		self.switch_togglePB7.setEnabled(True)
		self.switch_togglePB8.setEnabled(True)
		self.switch_togglePB9.setEnabled(True)
		self.switch_togglePB10.setEnabled(True)

		# uncheck KEYs and SWs
		self.key_togglePB1.setChecked(False)
		self.key_togglePB2.setChecked(False)
		self.key_togglePB3.setChecked(False)
		self.key_togglePB4.setChecked(False)
		self.switch_togglePB1.setChecked(False)
		self.switch_togglePB2.setChecked(False)
		self.switch_togglePB3.setChecked(False)
		self.switch_togglePB4.setChecked(False)
		self.switch_togglePB5.setChecked(False)
		self.switch_togglePB6.setChecked(False)
		self.switch_togglePB7.setChecked(False)
		self.switch_togglePB8.setChecked(False)
		self.switch_togglePB9.setChecked(False)
		self.switch_togglePB10.setChecked(False)

	def __setupArduino__(self):
		ports = list(serial.tools.list_ports.comports())
		arduinoPort = "COM4"

		for p in ports:
			if "Arduino" in p.description:
				arduinoPort = p.device

		try:
			self.ser = serial.Serial(port=arduinoPort,baudrate=9600,bytesize=serial.EIGHTBITS,timeout=1)
			print("Opened serial port {}, baudrate 9600 for Arduino.".format(arduinoPort))
			self.__arduinoPresent__()
			self.serialOpen = True
		except:
			print("No Arduino found.")
			self.__arduinoMissing__()
			self.serialOpen = False

	def __createStatus__(self):
		self.statusGroupBox = QGroupBox("Device Status")

		self.arduinoStatus = QLabel("Arduino Missing")
		self.arduinoReconnectButton = QPushButton("Check Arduino Connection")
		self.cameraStatus = QLabel("Camera Missing")
		self.cameraReconnectButton = QPushButton("Check Camera Connection")

		self.arduinoReconnectButton.clicked.connect(self.__setupArduino__)

		layout_1 = QVBoxLayout()
		layout_1.addWidget(self.arduinoStatus)
		layout_1.addWidget(self.arduinoReconnectButton)
		layout_1.addWidget(self.cameraStatus)
		layout_1.addWidget(self.cameraReconnectButton)

		self.statusGroupBox.setLayout(layout_1)

	def __setImage__(self, image):
		self.videoLabel.setPixmap(QPixmap.fromImage(image))

	def __createVideo__(self):
		self.videoGroupBox = QGroupBox("Live FPGA Video Feed")

		self.videoLabel = QLabel()
		self.videoLabel.resize(videoX,videoY)
		self.th = videoThread()
		self.th.changePixmap.connect(self.__setImage__)
		self.th.start()

		layout_1 = QVBoxLayout()
		layout_1.addStretch(1)
		layout_1.addWidget(self.videoLabel)
		layout_1.addStretch(1)

		layout_2 = QHBoxLayout()
		layout_2.addStretch(1)
		layout_2.addLayout(layout_1)
		layout_2.addStretch(1)

		self.videoGroupBox.setLayout(layout_2)

	def __uploadFileComplete__(self):
		self.statusLabel.setText("Status: Uploaded {}.".format(self.fileName))

	def __uploadFile__(self):
		self.statusLabel.setText("Status: Picking file...")
		filename = QFileDialog.getOpenFileName(None, "Open File", "C:\\","Programming Files (*.sof)")

		if(filename[0] != ""):
			self.statusLabel.setText("Status: Uploading file...")
			self.fileName = filename[0]
			sofFile = "p;"+filename[0]+"@2"
			print(sofFile)
			self.pgmThread = pgmThread(sofFile)
			self.pgmThread.uploadComplete.connect(self.__uploadFileComplete__)
			self.pgmThread.start()
			# quartus_pgm -m jtag -o "p;path/to/file.sof@2” 
		else:
			print("No file selected")
			self.statusLabel.setText("Status: No file selected.")

	def __createFileUploader__(self):
		self.fileUploaderGroupBox = QGroupBox("Program FPGA")

		filePickButton = QPushButton("Select .sof file and upload to FPGA")
		filePickButton.clicked.connect(self.__uploadFile__)
		self.statusLabel = QLabel("Status: No file selected.")

		layout_1 = QVBoxLayout()
		layout_1.addWidget(filePickButton)
		layout_1.addWidget(self.statusLabel)
		# layout_1.addStretch(0)

		# layout_2 = QHBoxLayout()
		# layout_2.addLayout(layout_1)
		# layout_2.addStretch(1)

		self.fileUploaderGroupBox.setLayout(layout_1)

	def __createSwitches__(self):
		self.switchGroupBox = QGroupBox("SW [0...9]")

		self.switch_togglePB1 = QPushButton("SW[0]")
		self.switch_togglePB2 = QPushButton("SW[1]")
		self.switch_togglePB3 = QPushButton("SW[2]")
		self.switch_togglePB4 = QPushButton("SW[3]")
		self.switch_togglePB5 = QPushButton("SW[4]")
		self.switch_togglePB6 = QPushButton("SW[5]")
		self.switch_togglePB7 = QPushButton("SW[6]")
		self.switch_togglePB8 = QPushButton("SW[7]")
		self.switch_togglePB9 = QPushButton("SW[8]")
		self.switch_togglePB10 = QPushButton("SW[9]")
		self.switch_togglePB1.setCheckable(True)
		self.switch_togglePB2.setCheckable(True)
		self.switch_togglePB3.setCheckable(True)
		self.switch_togglePB4.setCheckable(True)
		self.switch_togglePB5.setCheckable(True)
		self.switch_togglePB6.setCheckable(True)
		self.switch_togglePB7.setCheckable(True)
		self.switch_togglePB8.setCheckable(True)
		self.switch_togglePB9.setCheckable(True)
		self.switch_togglePB10.setCheckable(True)
		self.switch_togglePB1.setChecked(False)
		self.switch_togglePB2.setChecked(False)
		self.switch_togglePB3.setChecked(False)
		self.switch_togglePB4.setChecked(False)
		self.switch_togglePB5.setChecked(False)
		self.switch_togglePB6.setChecked(False)
		self.switch_togglePB7.setChecked(False)
		self.switch_togglePB8.setChecked(False)
		self.switch_togglePB9.setChecked(False)
		self.switch_togglePB10.setChecked(False)
		self.switch_togglePB1.setEnabled(False)
		self.switch_togglePB2.setEnabled(False)
		self.switch_togglePB3.setEnabled(False)
		self.switch_togglePB4.setEnabled(False)
		self.switch_togglePB5.setEnabled(False)
		self.switch_togglePB6.setEnabled(False)
		self.switch_togglePB7.setEnabled(False)
		self.switch_togglePB8.setEnabled(False)
		self.switch_togglePB9.setEnabled(False)
		self.switch_togglePB10.setEnabled(False)
		self.switch_togglePB1.clicked.connect(self.__SW0__)
		self.switch_togglePB2.clicked.connect(self.__SW1__)
		self.switch_togglePB3.clicked.connect(self.__SW2__)
		self.switch_togglePB4.clicked.connect(self.__SW3__)
		self.switch_togglePB5.clicked.connect(self.__SW4__)
		self.switch_togglePB6.clicked.connect(self.__SW5__)
		self.switch_togglePB7.clicked.connect(self.__SW6__)
		self.switch_togglePB8.clicked.connect(self.__SW7__)
		self.switch_togglePB9.clicked.connect(self.__SW8__)
		self.switch_togglePB10.clicked.connect(self.__SW9__)

		layout = QVBoxLayout()
		layout.addWidget(self.switch_togglePB10)
		layout.addWidget(self.switch_togglePB9)
		layout.addWidget(self.switch_togglePB8)
		layout.addWidget(self.switch_togglePB7)
		layout.addWidget(self.switch_togglePB6)
		layout.addWidget(self.switch_togglePB5)
		layout.addWidget(self.switch_togglePB4)
		layout.addWidget(self.switch_togglePB3)
		layout.addWidget(self.switch_togglePB2)
		layout.addWidget(self.switch_togglePB1)
		layout.addStretch(0)

		self.switchGroupBox.setLayout(layout)

	def __serialWrapper__(self, character):
		try:
			self.ser.write(character.encode())
		except:
			self.__setupArduino__()

	def __SW0__(self):
		if(self.switch_togglePB1.isChecked()):
			print("SW0 asserted")
			self.__serialWrapper__(")")
		else:
			print("SW0 deasserted")
			self.__serialWrapper__("*")

	def __SW1__(self):
		if(self.switch_togglePB2.isChecked()):
			print("SW1 asserted")
			self.__serialWrapper__("+")
		else:
			print("SW1 deasserted")
			self.__serialWrapper__(",")

	def __SW2__(self):
		if(self.switch_togglePB3.isChecked()):
			print("SW2 asserted")
			self.__serialWrapper__("-")
		else:
			print("SW2 deasserted")
			self.__serialWrapper__(".")

	def __SW3__(self):
		if(self.switch_togglePB4.isChecked()):
			print("SW3 asserted")
			self.__serialWrapper__("/")
		else:
			print("SW3 deasserted")
			self.__serialWrapper__("0")

	def __SW4__(self):
		if(self.switch_togglePB5.isChecked()):
			print("SW4 asserted")
			self.__serialWrapper__("1")
		else:
			print("SW4 deasserted")
			self.__serialWrapper__("2")

	def __SW5__(self):
		if(self.switch_togglePB6.isChecked()):
			print("SW5 asserted")
			self.__serialWrapper__("3")
		else:
			print("SW5 deasserted")
			self.__serialWrapper__("4")

	def __SW6__(self):
		if(self.switch_togglePB7.isChecked()):
			print("SW6 asserted")
			self.__serialWrapper__("5")
		else:
			print("SW6 deasserted")
			self.__serialWrapper__("6")

	def __SW7__(self):
		if(self.switch_togglePB8.isChecked()):
			print("SW7 asserted")
			self.__serialWrapper__("7")
		else:
			print("SW7 deasserted")
			self.__serialWrapper__("8")

	def __SW8__(self):
		if(self.switch_togglePB9.isChecked()):
			print("SW8 asserted")
			self.__serialWrapper__("9")
		else:
			print("SW7 deasserted")
			self.__serialWrapper__(":")

	def __SW9__(self):
		if(self.switch_togglePB10.isChecked()):
			print("SW9 asserted")
			self.__serialWrapper__(";")
		else:
			print("SW9 deasserted")
			self.__serialWrapper__("<")

	def __createKeys__(self):
		self.keyGroupBox = QGroupBox("KEY [0...3]")

		self.key_togglePB1 = QPushButton("KEY[0]")
		self.key_togglePB2 = QPushButton("KEY[1]")
		self.key_togglePB3 = QPushButton("KEY[2]")
		self.key_togglePB4 = QPushButton("KEY[3]")
		self.key_togglePB1.setCheckable(True)
		self.key_togglePB2.setCheckable(True)
		self.key_togglePB3.setCheckable(True)
		self.key_togglePB4.setCheckable(True)
		self.key_togglePB1.setChecked(False)
		self.key_togglePB2.setChecked(False)
		self.key_togglePB3.setChecked(False)
		self.key_togglePB4.setChecked(False)
		self.key_togglePB1.setEnabled(False)
		self.key_togglePB2.setEnabled(False)
		self.key_togglePB3.setEnabled(False)
		self.key_togglePB4.setEnabled(False)
		self.key_togglePB1.clicked.connect(self.__KEY0__)
		self.key_togglePB2.clicked.connect(self.__KEY1__)
		self.key_togglePB3.clicked.connect(self.__KEY2__)
		self.key_togglePB4.clicked.connect(self.__KEY3__)

		layout = QVBoxLayout()
		layout.addWidget(self.key_togglePB4)
		layout.addWidget(self.key_togglePB3)
		layout.addWidget(self.key_togglePB2)
		layout.addWidget(self.key_togglePB1)
		layout.addStretch(0)

		self.keyGroupBox.setLayout(layout)

	def __KEY0__(self):
		if(self.key_togglePB1.isChecked()):
			print("KEY0 asserted")
			self.__serialWrapper__("!")
		else:
			print("KEY0 deasserted")
			self.__serialWrapper__("\"")

	def __KEY1__(self):
		if(self.key_togglePB2.isChecked()):
			print("KEY1 asserted")
			self.__serialWrapper__("#")
		else:
			print("KEY1 deasserted")
			self.__serialWrapper__("$")

	def __KEY2__(self):
		if(self.key_togglePB3.isChecked()):
			print("KEY2 asserted")
			self.__serialWrapper__("%")
		else:
			print("KEY2 deasserted")
			self.__serialWrapper__("&")

	def __KEY3__(self):
		if(self.key_togglePB4.isChecked()):
			print("KEY3 asserted")
			self.__serialWrapper__("'")
		else:
			print("KEY3 deasserted")
			self.__serialWrapper__("(")

print("starting")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = GUI()
	win.show()
	exit_code = app.exec()
	
	if(win.serialOpen == True):
		win.ser.close()
		print("Closed serial port.")
	else:
		print("No serial port to close")
	
	win.th.quit()
	print("Quit video thread")
	exit(0)


