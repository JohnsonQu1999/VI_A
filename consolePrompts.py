import serial

class consolePrompts():
	def __init__(self):
		print("Initialized.")
		self.text = "This is the welcome prompt: Hello! :) <3"
		self.__welcomePrompts__()
		self.__control__()

	def __welcomePrompts__(self):
		print(self.text)

	def __control__(self):
		ser = serial.Serial(port='COM5',baudrate=9600,bytesize=serial.EIGHTBITS,timeout=1)

		print("Enter a character to send to the Arduino. Enter 'q' or 'Q' to quit.");
		charIn = str(input())
		# print(charIn[0])
		
		while(charIn != 'q' and charIn != 'Q'):
			ser.write(charIn[0].encode())
			print("Enter a character to send to the Arduino. Enter 'q' or 'Q' to quit.");
			charIn = str(input())

		ser.close()
		print("Quit.")

consolePrompts()

# print("test")
# num = int(input())
# print(num)