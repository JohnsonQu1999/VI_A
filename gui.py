from PyQt5.QtWidgets import (QApplication, QMainWindow, QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout,
	QLabel, QPushButton, QStyleFactory, QWidget)
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import sys
import serial
import cv2
import numpy as np

class Thread(QThread):
	changePixmap = pyqtSignal(QImage)

	def run(self):
		cap = cv2.VideoCapture(0)

		if(cap.isOpened() == False):
			print("Error opening video stream.")
			return

		while(True):
			ret, frame = cap.read()
			if(ret):
				rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				h, w, ch = rgbImage.shape
				bytesPerLine = ch*w
				convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
				p = convertToQtFormat.scaled(640,480,Qt.KeepAspectRatio)
				self.changePixmap.emit(p)

class GUI():
	def __init__(self, sysArgs = "COM6"):
		self.ser = serial.Serial(port=sys.argv[1],baudrate=9600,bytesize=serial.EIGHTBITS,timeout=1)
		print("Opened serial port {}, baudrate 9600".format(sys.argv[1]))

		app = QApplication(sys.argv)
		self.win = QMainWindow()
		self.win.setGeometry(100,100,1700,900)
		self.win.setWindowTitle("McMaster University Department of Computing and Software DE1-SoC Virtual Interface")

		# 1 make video placeholder
		self.__createVideo__()

		# 2 make key group
		self.__createKeys__()

		# 3 make switch group
		self.__createSwitches__()

		# 4 make file picker placeholder
		self.__createFileUploader__()

		# combine 2, 3, 4 into a vbox
		inputs_layout = QVBoxLayout()
		inputs_layout.addWidget(self.keyGroupBox)
		inputs_layout.addWidget(self.switchGroupBox)
		inputs_layout.addWidget(self.fileUploaderGroupBox)
		inputs_layout.addStretch(0)

		# # combine 1 into a vbox
		# outputs_layout = QVBoxLayout()
		# outputs_layout.addWidget(self.videoGroupBox)
		# outputs_layout.addStretch(1)

		# create the main gridlayout
		main_Layout = QGridLayout()
		main_Layout.addWidget(self.videoGroupBox, 0, 0)
		main_Layout.addLayout(inputs_layout, 0, 1)

		# create a widget, set the layout, and set the combination to the central widget
		centralWidget = QWidget()
		centralWidget.setLayout(main_Layout)
		self.win.setCentralWidget(centralWidget)
		self.win.show()

		exit_code = app.exec()
		self.ser.close()
		print("Closed serial port.")
		exit()
		print("exit")
		sys.exit(exit_code)

	def __setImage__(self, image):
		self.videoLabel.setPixmap(QPixmap.fromImage(image))

	def __createVideo__(self):
		self.videoGroupBox = QGroupBox("Live FPGA Video Feed")

		self.videoLabel = QLabel()
		self.videoLabel.resize(640,480)
		self.th = Thread()
		self.th.changePixmap.connect(self.__setImage__)
		self.th.start()

		layout = QVBoxLayout()
		layout.addWidget(self.videoLabel)
		layout.addStretch(1)

		self.videoGroupBox.setLayout(layout)

	def __createFileUploader__(self):
		self.fileUploaderGroupBox = QGroupBox("Choose your .sof file")

		label1 = QLabel("File Uploader Placeholder")

		layout = QVBoxLayout()
		layout.addWidget(label1)

		self.fileUploaderGroupBox.setLayout(layout)

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

		layout = QHBoxLayout()
		layout.addWidget(self.switch_togglePB1)
		layout.addWidget(self.switch_togglePB2)
		layout.addWidget(self.switch_togglePB3)
		layout.addWidget(self.switch_togglePB4)
		layout.addWidget(self.switch_togglePB5)
		layout.addWidget(self.switch_togglePB6)
		layout.addWidget(self.switch_togglePB7)
		layout.addWidget(self.switch_togglePB8)
		layout.addWidget(self.switch_togglePB9)
		layout.addWidget(self.switch_togglePB10)

		self.switchGroupBox.setLayout(layout)

	def __SW0__(self):
		if(self.switch_togglePB1.isChecked()):
			print("SW0 asserted")
			self.ser.write(")".encode())
		else:
			print("SW0 deasserted")
			self.ser.write("*".encode())

	def __SW1__(self):
		if(self.switch_togglePB2.isChecked()):
			print("SW1 asserted")
			self.ser.write("+".encode())
		else:
			print("SW1 deasserted")
			self.ser.write(",".encode())

	def __SW2__(self):
		if(self.switch_togglePB3.isChecked()):
			print("SW2 asserted")
			self.ser.write("-".encode())
		else:
			print("SW2 deasserted")
			self.ser.write(".".encode())

	def __SW3__(self):
		if(self.switch_togglePB4.isChecked()):
			print("SW3 asserted")
			self.ser.write("/".encode())
		else:
			print("SW3 deasserted")
			self.ser.write("0".encode())

	def __SW4__(self):
		if(self.switch_togglePB5.isChecked()):
			print("SW4 asserted")
			self.ser.write("1".encode())
		else:
			print("SW4 deasserted")
			self.ser.write("2".encode())

	def __SW5__(self):
		if(self.switch_togglePB6.isChecked()):
			print("SW5 asserted")
			self.ser.write("3".encode())
		else:
			print("SW5 deasserted")
			self.ser.write("4".encode())

	def __SW6__(self):
		if(self.switch_togglePB7.isChecked()):
			print("SW6 asserted")
			self.ser.write("5".encode())
		else:
			print("SW6 deasserted")
			self.ser.write("6".encode())

	def __SW7__(self):
		if(self.switch_togglePB8.isChecked()):
			print("SW7 asserted")
			self.ser.write("7".encode())
		else:
			print("SW7 deasserted")
			self.ser.write("8".encode())

	def __SW8__(self):
		if(self.switch_togglePB9.isChecked()):
			print("SW8 asserted")
			self.ser.write("9".encode())
		else:
			print("SW7 deasserted")
			self.ser.write(":".encode())

	def __SW9__(self):
		if(self.switch_togglePB10.isChecked()):
			print("SW9 asserted")
			self.ser.write(";".encode())
		else:
			print("SW9 deasserted")
			self.ser.write("<".encode())

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
		self.key_togglePB1.clicked.connect(self.__KEY0__)
		self.key_togglePB2.clicked.connect(self.__KEY1__)
		self.key_togglePB3.clicked.connect(self.__KEY2__)
		self.key_togglePB4.clicked.connect(self.__KEY3__)

		layout = QHBoxLayout()
		layout.addWidget(self.key_togglePB1)
		layout.addWidget(self.key_togglePB2)
		layout.addWidget(self.key_togglePB3)
		layout.addWidget(self.key_togglePB4)

		self.keyGroupBox.setLayout(layout)

	def __KEY0__(self):
		if(self.key_togglePB1.isChecked()):
			print("KEY0 asserted")
			self.ser.write("!".encode())
		else:
			print("KEY0 deasserted")
			self.ser.write("\"".encode())

	def __KEY1__(self):
		if(self.key_togglePB2.isChecked()):
			print("KEY1 asserted")
			self.ser.write("#".encode())
		else:
			print("KEY1 deasserted")
			self.ser.write("$".encode())

	def __KEY2__(self):
		if(self.key_togglePB3.isChecked()):
			print("KEY2 asserted")
			self.ser.write("%".encode())
		else:
			print("KEY2 deasserted")
			self.ser.write("&".encode())

	def __KEY3__(self):
		if(self.key_togglePB4.isChecked()):
			print("KEY3 asserted")
			self.ser.write("'".encode())
		else:
			print("KEY3 deasserted")
			self.ser.write("(".encode())


print("working")


GUI()