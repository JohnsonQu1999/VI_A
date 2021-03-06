from PyQt5.QtWidgets import (QApplication, QMainWindow, QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout,
	QLabel, QPushButton, QStyleFactory, QWidget, QFileDialog, QMessageBox)
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap			# To make GUI.
import sys 										# To take command line arguments. No 
import serial 									# To communicate with Arduino.
import serial.tools.list_ports 					# To list available ports. Used to auto-detect Arduino.
import cv2										# To get video.
import numpy as np 								# OpenCV needs this.
import subprocess								# To start new processes. Used to program the FPGA via quartus_pgm.

videoX = 1504		# Optimized for a 1920x1080 screen. Change as necessary.
videoY = 846		# Optimized for a 1920x1080 screen. Change as necessary.

class videoThread(QThread):
	# Signals
	changePixmap = pyqtSignal(QImage)	# Emited when a new frame is available.
	videoMissingSignal = pyqtSignal()	# Emitted when frames are unavailable. Usually caused by a busy or missing camera.
	videoPresentSignal = pyqtSignal()	# Emitted if camera setup is successful.

	def run(self):
		cap = cv2.VideoCapture(0)

		if(cap.isOpened() == False):
			cap.release()
			self.videoMissingSignal.emit()
			return

		self.videoPresentSignal.emit()

		cap.set(3, videoX)		# PropID 3 = CV_CAP_PROP_FRAME_WIDTH
		cap.set(4, videoY)		# PropID 4 = CV_CAP_PROP_FRAME_HEIGHT
		print("Video running at {}fps".format(cap.get(5)))

		while(True):
			returnValue, frame = cap.read()
			if(returnValue):
				rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				h, w, ch = rgbImage.shape
				bytesPerLine = ch*w
				convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
				p = convertToQtFormat.scaled(videoX,videoY,Qt.KeepAspectRatio)
				self.changePixmap.emit(p)
				flat = 0
			else:
				break 		# Break out of loop if return value == False. The loop must be broken out of or else the QThread will never quit and cap will never stop trying to read.

		cap.release()
		self.videoMissingSignal.emit()

class pgmThread(QThread):
	# Signals 
	uploadSuccess = pyqtSignal()		# Emitted if a return code of 0 is received
	uploadFailure = pyqtSignal(int)		# Emitted if a non-zero return code is received. The return code is sent.

	def __init__(self, sofFile):
		QThread.__init__(self)
		self.sofFile = sofFile

	def run(self):
		try:
			result = subprocess.run(["quartus_pgm","-m","jtag","-o",self.sofFile])
			# quartus_pgm -m jtag -o "p;path/to/file.sof@2”		<-- this is how you would enter the quartus_pgm command in command line.
			if(result.returncode == 0):
				self.uploadSuccess.emit()
			else:
				self.uploadFailure.emit(result.returncode)
		except:
			self.uploadFailure.emit(-1)

class GUI(QMainWindow):
	def __init__(self):
		# Control variables
		self.serialOpen = False
		self.arduinoCounter = False		# Quick and dirty solution. Display an info box when the arduino is successfully reconnected, but not upon initial start up by seeing if "__arduinoPresent__" was signaled. There's probably a better way.
		self.videoCounter = False		# Quick and dirty solution. Display an info box when the video is successfully reconnected, but not upon initial start up by seeing if "__videoPresent__" was signaled. There's probably a better way.

		# QMainWindow setup
		QMainWindow.__init__(self)
		self.setGeometry(100,100,1700,900)
		self.setWindowTitle("McMaster University Department of Computing and Software DE1-SoC Virtual Interface")
		self.setStyleSheet("QLabel {font: 14pt Calibri}" + "QPushButton {font: 14pt Calibri}" + "QGroupBox {font: 20pt Calibri}")

		# \begin{Layout setup}
		# 1 make video group
		self.__createVideoGroupBox__()
		# 2 make key group
		self.__createKeysGroupBox__()
		# 3 make switch group
		self.__createSwitchesGroupBox__()
		# 4 make file upload group 
		self.__createFileUploaderGroupBox__()
		# 5 make arduino/camera status group
		self.__createStatusGroupBox__()
		#
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
		#
		# create a widget, set the layout, and set the combination to the central widget
		centralWidget = QWidget()
		centralWidget.setLayout(main_Layout)
		self.setCentralWidget(centralWidget)
		# \end{Layout setup}

		# Setting up hardware that could break while the application runs. The application is intended to recover gracefully and even restore functionality if hardware is restored.
		# Practically, this means: Sending a signal while the arduino is unplugged won't crash the program - the user can try reconnecting to the arduino.
		# Unplugging the camera won't crash the program - the user can try reconnecting. Similar behaviour if the camera is occupied.
		# Unsuccessful programming will result in a notification to the user - the user can try reconnecting to the FPGA.
		self.__setupArduino__()
		self.__setupVideoThread__()

	def __arduinoMissing__(self):
		# update serial status
		self.serialOpen = False

		# update arduino device status
		self.arduinoStatus.setText("Arduino Status: Failure")

		# deactivate check arduino button
		self.arduinoReconnectButton.setEnabled(True)

		# deactivate KEYs and SWs
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

		# Error message
		errMsgArduinoM = QMessageBox()
		errMsgArduinoM.setIcon(QMessageBox.Critical)
		errMsgArduinoM.setText("Arduino Serial Unavailable")
		errMsgArduinoM.setInformativeText("Try pressing the 'Check Arduino Connection' button. If the error persists, contact a TA to check the physical connection.")
		errMsgArduinoM.setWindowTitle("Arduino Serial Error")
		errMsgArduinoM.setDetailedText("WANTED: ARDUINO FOR FAILURE TO CONNECT.")

		print("Arduino Missing return value: {}.".format(errMsgArduinoM.exec()))

	def __arduinoPresent__(self):
		# update serial status
		self.serialOpen = True

		# update arduino device status
		self.arduinoStatus.setText("Arduino Status: Working")

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

		# Info message
		if(self.arduinoCounter == True):
			infoMsgArduinoP = QMessageBox()
			infoMsgArduinoP.setIcon(QMessageBox.Information)
			infoMsgArduinoP.setText("Arduino Serial Reconnected")
			infoMsgArduinoP.setWindowTitle("Success")
			infoMsgArduinoP.setDetailedText("CAPTURED: ARDUINO FOR FAILURE TO CONNECT.")

			print("Arduino Present return value: {}.".format(infoMsgArduinoP.exec()))

		self.arduinoCounter = True

	def __setupArduino__(self):
		ports = list(serial.tools.list_ports.comports())
		arduinoPort = "COM7"

		for p in ports:
			if "Arduino" in p.description:
				arduinoPort = p.device

		try:
			self.ser = serial.Serial(port=arduinoPort,baudrate=9600,bytesize=serial.EIGHTBITS,timeout=1)
			print("Arduino: Opened serial port {}, baudrate 9600.".format(arduinoPort))
			self.__arduinoPresent__()
		except:
			print("No Arduino found.")
			self.__arduinoMissing__()

	def __setImage__(self, image):
		self.videoLabel.setPixmap(QPixmap.fromImage(image))

	def __videoMissing__(self):
		print("Video Missing")

		# update video status
		self.videoOpen = True

		# update video device status
		self.videoStatus.setText("Video Status: Failure")

		# deactivate check video button
		self.videoReconnectButton.setEnabled(True)

		# Quit video thread
		self.videoThread.quit()
		print("QThread is Finished?: {}".format(self.videoThread.isFinished()))

		# Error message
		errMsgVideoM = QMessageBox()
		errMsgVideoM.setIcon(QMessageBox.Critical)
		errMsgVideoM.setText("Video Feed Unavailable")
		errMsgVideoM.setInformativeText("Try pressing the 'Check Video Connection' button. If the error persists, contact a TA to check the physical connection.")
		errMsgVideoM.setWindowTitle("Video Capture Error")
		errMsgVideoM.setDetailedText("Video Feed Evaporated. Get a condenser from the nearest refrigerator!")

		print("Video Missing return value: {}.".format(errMsgVideoM.exec()))

	def __videoPresent__(self):
		print("Video Present.")

		# update video status
		self.videoOpen = True

		# update video device status
		self.videoStatus.setText("Video Status: Working")

		# activate check video button
		self.videoReconnectButton.setEnabled(False)

		# Info message
		if(self.videoCounter == True):
			infoMsgVideoP = QMessageBox()
			infoMsgVideoP.setIcon(QMessageBox.Information)
			infoMsgVideoP.setText("Video Reconnected")
			infoMsgVideoP.setWindowTitle("Success")
			infoMsgVideoP.setDetailedText("Good job! Condenser successfully installed.")

			print("Video Present return value: {}.".format(infoMsgVideoP.exec()))
		else:
			infoMsgVideoP = QMessageBox()
			infoMsgVideoP.setIcon(QMessageBox.Information)
			infoMsgVideoP.setText("Video Connected. Please wait up to 30 seconds for video feed to appear.")
			infoMsgVideoP.setWindowTitle("Success")

			print("Video Present return value: {}.".format(infoMsgVideoP.exec()))

		self.videoCounter = True

	def __setupVideoThread__(self):
		self.videoThread = videoThread()
		self.videoThread.changePixmap.connect(self.__setImage__)			# Grabs new frames
		self.videoThread.videoMissingSignal.connect(self.__videoMissing__)	# Updates system variables and GUI
		self.videoThread.videoPresentSignal.connect(self.__videoPresent__)	# Updates system variables and GUI

		self.videoThread.start()

	def __restartVideoThread__(self):
		self.videoReconnectButton.setEnabled(False)
		self.videoThread.start()

	def __createVideoGroupBox__(self):
		self.videoGroupBox = QGroupBox("Live FPGA Video Feed")

		self.videoLabel = QLabel()
		self.videoLabel.resize(videoX,videoY)

		layout_1 = QVBoxLayout()
		layout_1.addStretch(1)
		layout_1.addWidget(self.videoLabel)
		layout_1.addStretch(1)

		layout_2 = QHBoxLayout()
		layout_2.addStretch(1)
		layout_2.addLayout(layout_1)
		layout_2.addStretch(1)

		self.videoGroupBox.setLayout(layout_2)

	def __uploadFileFailure__(self, returncode):
		self.statusLabel.setText("Status: Upload Failure with return code {}.".format(returncode))

		# Error message
		errMsgFileF = QMessageBox()
		errMsgFileF.setIcon(QMessageBox.Warning)
		errMsgFileF.setText("File Upload Failed")
		errMsgFileF.setInformativeText("File Upload Failed with return code {}. Ensure that you are uploading a valid .sof file. If the error persists, contact a TA to check the physical connection.".format(returncode))
		errMsgFileF.setWindowTitle("File Upload Error")
		errMsgFileF.setDetailedText("""Unable to Upload File. Grab a spare from your toolbox.
			Return codes:
			0 - Execution was successful.
			2 - Execution failed due to an internal error.
			3 - Execution failed due to user error(s). Common cause: Programming cable not connected.
			4 - Execution was stopped by user.
			-1 - Non-Quartus (custom) return code. Exception was thrown.
			""")

		print("File Failure return value: {}.".format(errMsgFileF.exec()))

	def __uploadFileSuccess__(self):
		self.statusLabel.setText("Status: Uploaded {}.".format(self.fileName))

		# Info message
		if(self.arduinoCounter == True):
			infoMsgArduinoP = QMessageBox()
			infoMsgArduinoP.setIcon(QMessageBox.Information)
			infoMsgArduinoP.setText("File Successfully Uploaded")
			infoMsgArduinoP.setWindowTitle("Success")

			print("Upload File Success return value: {}.".format(infoMsgArduinoP.exec()))

	def __uploadFile__(self):
		self.statusLabel.setText("Status: Picking file...")
		filename = QFileDialog.getOpenFileName(None, "Open File", "C:\\","Programming Files (*.sof)")

		if(filename[0] != ""):
			self.statusLabel.setText("Status: Uploading file...")
			self.fileName = filename[0]
			sofFile = "p;"+filename[0]+"@2"
			print(sofFile)
			self.pgmThread = pgmThread(sofFile)
			self.pgmThread.uploadSuccess.connect(self.__uploadFileSuccess__)
			self.pgmThread.uploadFailure.connect(self.__uploadFileFailure__)
			self.pgmThread.start()
		else:
			print("No file selected")
			self.statusLabel.setText("Status: No file selected.")

	def __createFileUploaderGroupBox__(self):
		self.fileUploaderGroupBox = QGroupBox("Program FPGA")

		filePickButton = QPushButton("Select .sof file and upload to FPGA")
		filePickButton.clicked.connect(self.__uploadFile__)
		self.statusLabel = QLabel("Status: No file selected.")
		self.statusLabel.setWordWrap(True)

		layout_1 = QVBoxLayout()
		layout_1.addWidget(filePickButton)
		layout_1.addWidget(self.statusLabel)

		self.fileUploaderGroupBox.setLayout(layout_1)

	def __createStatusGroupBox__(self):
		self.statusGroupBox = QGroupBox("Device Status")

		self.arduinoStatus = QLabel("Arduino Status: Loading...")
		self.arduinoReconnectButton = QPushButton("Check Arduino Connection")
		self.arduinoReconnectButton.setEnabled(False)
		self.videoStatus = QLabel("Camera Status: Loading...")
		self.videoReconnectButton = QPushButton("Check Video Connection")
		self.videoReconnectButton.setEnabled(False)

		self.arduinoReconnectButton.clicked.connect(self.__setupArduino__)
		self.videoReconnectButton.clicked.connect(self.__restartVideoThread__)

		layout_1 = QVBoxLayout()
		layout_1.addWidget(self.arduinoStatus)
		layout_1.addWidget(self.arduinoReconnectButton)
		layout_1.addWidget(self.videoStatus)
		layout_1.addWidget(self.videoReconnectButton)

		self.statusGroupBox.setLayout(layout_1)

	def __createSwitchesGroupBox__(self):
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

	def __serialWrapper__(self, character, mode, hardware):
		try:
			self.ser.write(character.encode())
			if(mode == 0):
				print("{} asserted.".format(hardware))
			elif(mode == 1):
				print("{} deasserted.".format(hardware))
			else:
				print("Unexpected mode.")
		except:
			self.__setupArduino__()

	def __SW0__(self):
		if(self.switch_togglePB1.isChecked()):
			self.__serialWrapper__(")",0,"SW0")
		else:
			self.__serialWrapper__("*",1,"SW0")

	def __SW1__(self):
		if(self.switch_togglePB2.isChecked()):
			self.__serialWrapper__("+",0,"SW1")
		else:
			self.__serialWrapper__(",",1,"SW1")

	def __SW2__(self):
		if(self.switch_togglePB3.isChecked()):
			self.__serialWrapper__("-",0,"SW2")
		else:
			self.__serialWrapper__(".",1,"SW2")

	def __SW3__(self):
		if(self.switch_togglePB4.isChecked()):
			self.__serialWrapper__("/",0,"SW3")
		else:
			self.__serialWrapper__("0",1,"SW3")

	def __SW4__(self):
		if(self.switch_togglePB5.isChecked()):
			self.__serialWrapper__("1",0,"SW4")
		else:
			self.__serialWrapper__("2",1,"SW4")

	def __SW5__(self):
		if(self.switch_togglePB6.isChecked()):
			self.__serialWrapper__("3",0,"SW5")
		else:
			self.__serialWrapper__("4",1,"SW5")

	def __SW6__(self):
		if(self.switch_togglePB7.isChecked()):
			self.__serialWrapper__("5",0,"SW6")
		else:
			self.__serialWrapper__("6",1,"SW6")

	def __SW7__(self):
		if(self.switch_togglePB8.isChecked()):
			self.__serialWrapper__("7",0,"SW7")
		else:
			self.__serialWrapper__("8",1,"SW7")

	def __SW8__(self):
		if(self.switch_togglePB9.isChecked()):
			self.__serialWrapper__("9",0,"SW8")
		else:
			self.__serialWrapper__(":",1,"SW8")

	def __SW9__(self):
		if(self.switch_togglePB10.isChecked()):
			self.__serialWrapper__(";",0,"SW9")
		else:
			self.__serialWrapper__("<",1,"SW9")

	def __createKeysGroupBox__(self):
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
			self.__serialWrapper__("!",0,"KEY0")
		else:
			self.__serialWrapper__("\"",1,"KEY0")

	def __KEY1__(self):
		if(self.key_togglePB2.isChecked()):
			self.__serialWrapper__("#",0,"KEY1")
		else:
			self.__serialWrapper__("$",1,"KEY1")

	def __KEY2__(self):
		if(self.key_togglePB3.isChecked()):
			self.__serialWrapper__("%",0,"KEY2")
		else:
			self.__serialWrapper__("&",1,"KEY2")

	def __KEY3__(self):
		if(self.key_togglePB4.isChecked()):
			self.__serialWrapper__("'",0,"KEY3")
		else:
			self.__serialWrapper__("(",1,"KEY3")

print("Starting.")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle("Fusion")

	win = GUI()
	win.show()
	exit_code = app.exec()
	
	if(win.serialOpen == True):
		win.ser.close()
		print("Closed serial port.")
	else:
		print("No serial port to close.")
	
	win.videoThread.exit()
	print("Quit video thread.")
	print("Exit_code: {}.".format(exit_code))
	exit(0)