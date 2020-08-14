from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)     # Inherits QDialog. Not realy sure what the two arguments being passed do.

        # Saving the look of the program
        self.originalPalette = QApplication.palette()   # Remembers the original palette so the "Use Style's standard palette" checkbox is useful.

        # Creating drop down menus, checkboxes, labels, etc
        styleComboBox = QComboBox()                     # Makes the combobox. Doesn't make it self yet b/c we'll add it to self later.
        styleComboBox.addItems(QStyleFactory.keys())    # Adds the GUI styles stored by QStyleFactory by calling the keys method.

        styleLabel = QLabel("&Style:")                  # Creates the "Style" label. If you prepend the label with & and you assign a buddy to the label, if you press alt + the character
                                                        # after the & it'll let you control the combobox with your keyboard.
        styleLabel.setBuddy(styleComboBox)              # Adds the style combo box filled by the GUI style keys as the label's buddy.

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")       # Create a checkbox with text & allow alt + u to toggle it
        self.useStylePaletteCheckBox.setChecked(True)                                   # toggle it by default

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")  # Create a checkbox with text and allow alt + d to toggle it

        # Creating groups of widgets
        self.createTopLeftGroupBox()        # Call a bunch of methods that make certain widgets/groups/layouts
        self.createTopRightGroupBox()       # Call a bunch of methods that make certain widgets/groups/layouts
        self.createBottomLeftTabWidget()    # Call a bunch of methods that make certain widgets/groups/layouts
        self.createBottomRightGroupBox()    # Call a bunch of methods that make certain widgets/groups/layouts
        self.createProgressBar()            # Call a bunch of methods that make certain widgets/groups/layouts

        # Connecting signals to slots
        styleComboBox.activated[str].connect(self.changeStyle)                          # .activated is a signal. .connect sets the slot that it controls, which is changeStyle.
                                                                                        # changeStyle is a custom method that sets the style of the QApplication to something. I guess
                                                                                        # the combobox must send the current value to self.changestyle which is how it figures out what to 
                                                                                        # do. https://www.reddit.com/r/learnpython/comments/5h7mgn/i_dont_understand_the_brackets_in/
                                                                                        # So the .connect tells the combobox that when the activated signal is asserted, to call changestyle
                                                                                        # Also, activated[str] is a dictionary. The other option is to have activated[int].
                                                                                        # So now it knows that when it's activated, type string, to send that string to self.changestyle
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)                # When the checkbox is toggled, that signal calls the slot changePalette which
                                                                                        # performs and action depending on if the checkbox is checked or not
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)        # When the disable widgets checkbox is toggled, that signal calls the method
                                                                                        # topLeftGroupBox.setdisabled which disables that widget of type QGroupBox
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)       # connects the toggle signal for the disable widgets checkbox to something I don't quite understand
                                                                                        # Alternative way: https://gis.stackexchange.com/questions/201732/enable-groupbox-only-when-checkbox-is-checked-pyqgis
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)    # same as above
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)    # same as above

        # Building the top bar layout
        topLayout = QHBoxLayout()                           # Start with an Hbox
        topLayout.addWidget(styleLabel)                     # add the label "style"
        topLayout.addWidget(styleComboBox)                  # add the style combobox
        topLayout.addStretch(1)                             # add an empty stretchable box
        topLayout.addWidget(self.useStylePaletteCheckBox)   # add the checkbox "use style"
        topLayout.addWidget(disableWidgetsCheckBox)         # add the checkbox "disable widgets"

        # Building the rest of the layout
        mainLayout = QGridLayout()                          # Start with a GridLayout
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)         # add the top layout at the 0th row and 0th column having 1 row span and 2 column span
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)    # add the first group to the 1st row and 0th column (starts counting from 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)   # add the second group to the 1st row and 1st column
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)# add the widget box to the 2nd row and 0th column
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)# add the third group to the 2nd row and 1st column
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)  # add the progress bar to the 3rd row and 0th column having 1 row span and 2 column span
        mainLayout.setRowStretch(1, 1)                      # sets the 1st row to a stretch factor of 1 relative to the other rows
        mainLayout.setRowStretch(2, 1)                      # sets the 2nd row to a stretch factor of 1 relative to the other rows
        mainLayout.setColumnStretch(0, 1)                   # sets the 0th column to a stretch factor of 1 relative to the other columns
        mainLayout.setColumnStretch(1, 1)                   # sets the 1st column to a stretch factor of 1 relative to the other columns
        self.setLayout(mainLayout)                          # set the layout to "main layout"

        self.setWindowTitle("Styles")                       # set the name for the program title
        self.changeStyle('Windows')                         # set the default style to windows

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")     # Make a QGroupBox

        radioButton1 = QRadioButton("Radio button 1")   # make a radio button
        radioButton2 = QRadioButton("Radio button 2")   # "
        radioButton3 = QRadioButton("Radio button 3")   # "
        radioButton1.setChecked(True)                   # Set default to the first one checked

        checkBox = QCheckBox("Tri-state check box")     # make a tri state checkbox
        checkBox.setTristate(True)                      # set the default state to true
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()          # make a VBox
        layout.addWidget(radioButton1)  # add the radio button                
        layout.addWidget(radioButton2)  # "
        layout.addWidget(radioButton3)  # "
        layout.addWidget(checkBox)      # add the checkbox
        layout.addStretch(1)            # add a stretchable box at the end
        self.topLeftGroupBox.setLayout(layout)  # make this the layout for the groupbox

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 