# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# app = QApplication([])
# app.setStyle('Fusion')
# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QPushButton('Top'))
# layout.addWidget(QPushButton('Bottom'))
# window.setLayout(layout)
# window.show()
# app.exec()

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
import sys

class tutorial():
	def __init__(self):
		self.app = QApplication(sys.argv)
		
		self.win = QMainWindow()
		self.win.setGeometry(400,400,500,300)
		self.win.setWindowTitle("My First Qt Program")
		
		self.label = QLabel(self.win)
		self.label.setText("GUI Application with PyQt5")
		self.label.adjustSize()
		self.label.move(100,100)

		self.button = QPushButton(self.win)
		self.button.clicked.connect(self.update)
		self.button.setText("Update Button")
		self.button.move(100,150)

		self.button2 = QPushButton(self.win)
		self.button2.clicked.connect(self.retrieve)
		self.button2.setText("Retrieve Button")
		self.button2.move(100,200)

		self.button3 = QPushButton(self.win)
		self.button3.clicked.connect(self.win.close)
		self.button3.setText("Quit Button")
		self.button3.resize(120,60)
		self.button3.move(350,220)
		self.button3.setIcon(QtGui.QIcon("Cropped.jpg"))

		self.win.show()
		sys.exit(self.app.exec())
	
	def update(self):
		self.label.setText("Updated")

	def retrieve(self):
		print(self.label.text())



tutorial()