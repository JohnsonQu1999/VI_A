from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QPushButton, QWidget, QApplication
import sys

class test(QWidget):
	def __init__(self, parent = None):
		super(test, self).__init__(parent)

		self.setGeometry(100,100,600,400)

		layout = QVBoxLayout()

		self.btn = QPushButton("Static")
		self.btn.clicked.connect(self.getFile)

		layout.addWidget(self.btn)

		self.setLayout(layout)

	def getFile(self):
		filename = QFileDialog.getOpenFileName(self, "Open File", "C:\\","Image files (*.jpg *.gif)")
		print(filename[0])

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = test()
	ex.show()
	sys.exit(app.exec())

# filename = QFileDiaog.getOpenFileName()