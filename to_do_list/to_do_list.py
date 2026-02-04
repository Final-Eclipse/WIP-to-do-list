from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QSizePolicy, QVBoxLayout, QLabel, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QGraphicsEffect, QTextEdit,
                             QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF, QTimer, QDateTime, QDate, pyqtSignal, QUrl, QSize
from PyQt5.QtGui import QFont, QLinearGradient, QPainter, QBrush, QPen, QColor, QPixmap, QDesktopServices
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from datetime import datetime
import json

# In self.save_to_do_input_to_file, add inputs to a dictionary and append to a json file.
# Sort the dictionary using the to_do_inputs index in self.to_do_inputs as the dictionary key.
# Have each key's value be the respective input's text.
# Change the text of each input field to their dictionary value when opening application.

# Make button and input field more transparent when completing it.
# Make button and input field less transparent when uncompleting it.
# Make transparent color grey as more transparent does not stand out very much.

# Save whether or not a to-do has been completed and save the date as well.

# Disable input fields when to-do is set as completed.

# When starting app, set the input fields to complete or not complete based on the "completion_status" in the json file.
# Along with setting the "completion_status" in the json file, add a key for "date_completed".
# This date will be loaded when the app starts.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.buttons = []
        self.to_do_inputs = []
        self.date_completed_labels = []

        self.initUI()

    def initUI(self):
        # Creating layout and setting its properties.
        main_layout = QGridLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 10)

        # Set window properties.
        self.setFixedSize(800, 800)
        self.setWindowTitle("To-do List")

        # Create title label.
        title_label = QLabel()
        title_label.setText("To-do List")
        title_label.setFont(QFont("Californian FB", 30, QFont.Medium))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label, 0, 0, 1, 2)

        # Create to-do list area.
        todos_area_layout = QGridLayout()
        todos_area_widget = QWidget()
        todos_area_widget.setLayout(todos_area_layout)
        main_layout.addWidget(todos_area_widget, 1, 0, 1, 2)

        # Use multiples of two for start:stop indices.
        for x in range(0, 14):
            if x % 2 == 0:
                button = self.create_button()
                todos_area_layout.addWidget(button, x, 0, 1, 1)

                to_do_input = self.create_to_do_input()
                todos_area_layout.addWidget(to_do_input, x, 1, 1, 10)
            else:
                date_completed_label = self.create_date_completed_label()
                todos_area_layout.addWidget(date_completed_label, x, 5, 1, 2)
        
        self.set_to_do_input_text()

    def paintEvent(self, a0):
        """Creates and sets a gradiant background."""
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 0, Qt.SolidLine))

        gradiant = QLinearGradient(0, 0, 0, self.height())  # start at x1, y1, and end at x2, y2 
        gradiant.setColorAt(0, QColor("#aed1ef"))
        gradiant.setColorAt(0.5, QColor("#f2dfc1"))
        gradiant.setColorAt(1, QColor("#f0b9ef"))

        painter.setBrush(QBrush(gradiant))
        painter.drawRect(0, 0, self.width(), self.height())
    
    def create_date_completed_label(self):
        date_completed_label = QLabel()
        date_completed_label.setFont(QFont("Arial", 10, QFont.Medium))
        date_completed_label.setAlignment(Qt.AlignRight)
        date_completed_label.setFixedSize(400, 39)
        self.date_completed_labels.append(date_completed_label)

        return date_completed_label

    def save_to_do_input_to_file(self):
        with open("to_do_list.json", "r+") as file:
            file_contents = file.read()

            if file_contents == "":
                file.write(json.dumps({}))
                file.seek(0)
                file_contents = file.read()
           
            data = json.loads(file_contents)
            file.seek(0)

            index_key = str(self.to_do_inputs.index(self.sender()))
            
            if data.get(index_key) == None:
                data[index_key] = {}
            else:
                data[index_key]["text"] = self.sender().text()

            data = json.dumps(data, indent=2)

            file.write(data)
            file.truncate()

    def get_to_do_input_text(self):
        with open("to_do_list.json", "r") as file:
            file_contents = file.read()

        if file_contents == "":
            return {}
        else:
            return json.loads(file_contents)

    def set_to_do_input_text(self):
        input_text = self.get_to_do_input_text()

        try:
            for index, input in enumerate(self.to_do_inputs):
                input.setText(input_text[str(index)]["text"])
        except KeyError:
            pass

    def connect_to_do_input_to_slot(self, to_do_input):
        to_do_input.textChanged.connect(self.save_to_do_input_to_file)

    def create_to_do_input(self):
        to_do_input = QLineEdit()
        to_do_input.setStyleSheet("background-color: rgba(255, 255, 255, 120)")
        to_do_input.setFont(QFont("Arial", 30, QFont.Medium))

        to_do_input.setFixedSize(701, 51)

        self.to_do_inputs.append(to_do_input)
        self.connect_to_do_input_to_slot(to_do_input)

        return to_do_input

    def connect_button_to_slot(self, button):
        button.clicked.connect(self.change_button_properties)
        button.clicked.connect(self.set_date_completed)
        button.clicked.connect(self.save_completion_status_to_file)

    def save_completion_status_to_file(self):
        with open("to_do_list.json", "r+") as file:
            file_contents = file.read()

            if file_contents == "":
                file.write(json.dumps({}))
                file.seek(0)
                file_contents = file.read()
           
            data = json.loads(file_contents)
            file.seek(0)

            index_key = str(self.buttons.index(self.sender()))

            if data.get(index_key) == None:
                data[index_key] = {}

            if data[index_key].get("completion_status") == True:
                data[index_key]["completion_status"] = False

            elif data[index_key].get("completion_status") == False:
                data[index_key]["completion_status"] = True
                
            else:
                data[index_key]["completion_status"] = True

            data = json.dumps(data, indent=2)

            file.write(data)
            file.truncate()
    
    def set_date_completed(self):
        date = QDate.currentDate().toString()

        index = self.buttons.index(self.sender())
        date_completed_label = self.date_completed_labels[index]

        if date_completed_label.text() == "":
            date_completed_label.setText(f"Completed on {date}")
        else:
            date_completed_label.setText("")

    def create_button(self):
        button = QPushButton("✗")
        button.setStyleSheet("background-color: rgba(255, 255, 255, 120)")
        button.setFont(QFont("Arial", 28, QFont.Medium))

        button.setFixedSize(69, 50)

        self.buttons.append(button)
        self.connect_button_to_slot(button)

        return button

    def change_button_properties(self):
        button = self.sender()
        button_text = self.sender().text()

        if button_text == "✗":
            button.setText("✓") 
            button.setStyleSheet("background-color: rgba(255, 255, 255, 10)")
        elif button_text == "✓":
            button.setText("✗")
            button.setStyleSheet("background-color: rgba(255, 255, 255, 120)")

        self.change_to_do_input_properties(button)
    
    def change_to_do_input_properties(self, button):
        if button.text() == "✓":
            self.to_do_inputs[self.buttons.index(self.sender())].setStyleSheet("background-color: rgba(255, 255, 255, 10)")
        elif button.text() == "✗":
            self.to_do_inputs[self.buttons.index(self.sender())].setStyleSheet("background-color: rgba(255, 255, 255, 120)")

    # def init_button_properties(self):
    #     file_json = self.get_to_do_input_text()

        # index_key = str(self.buttons.index(self.sender()))

        # for button in self.buttons:
        #     file_json[]

    # def get_completion_status(self):
    #     with open("to_do_list.json", "r") as file:
    #         file_contents = json.loads(file.read())

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
