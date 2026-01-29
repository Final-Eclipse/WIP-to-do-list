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
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.buttons = []
        self.to_do_inputs = []

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
        self.setStyleSheet("background-color: blue")
        self.setFixedSize(800, 800)

        # Create title label.
        self.title_label = QLabel()
        self.title_label.setText("To-do List")
        self.title_label.setStyleSheet("background-color: pink; font-size: 20px")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label, 0, 0, 1, 2)

        # Create to-do list area.
        self.todos_area_layout = QGridLayout()
        self.todos_area_widget = QWidget()
        self.todos_area_widget.setLayout(self.todos_area_layout)
        self.todos_area_widget.setStyleSheet("background-color: #e6fd93")
        main_layout.addWidget(self.todos_area_widget, 1, 0, 1, 2)

        # Creates a specified number of buttons and text areas
        for x in range(0, 5):
            button = self.create_button()
            self.todos_area_layout.addWidget(button, x, 0, 1, 1)

            to_do_input = self.create_to_do_input()
            self.todos_area_layout.addWidget(to_do_input, x, 1, 1, 10)

    def save_to_do_input_to_file(self):
        # with open("to_do_list.txt", "r+") as file:
        #     file_contents = file.read()
        #     if file_contents == "":
        #         print("empty")
        #         file.write(json.dumps({}))

        current_input = self.sender().text()
        with open("to_do_list.txt", "r+") as file:
            file_contents = file.read()
            if file_contents == "":
                print("empty")
                file.write(json.dumps({}))
            else:
                file.seek(0)
                file.write(current_input)

    def connect_to_do_input_to_slot(self, to_do_input):
        to_do_input.textChanged.connect(self.save_to_do_input_to_file)

    def create_to_do_input(self):
        to_do_input = QLineEdit()
        to_do_input.setStyleSheet("background-color: #60ffcf")
        to_do_input.setFont(QFont("Arial", 30, QFont.Medium))

        self.to_do_inputs.append(to_do_input)
        self.connect_to_do_input_to_slot(to_do_input)

        return to_do_input

    def connect_button_to_slot(self, button):
        button.clicked.connect(self.change_button_properties)

    def create_button(self):
        button = QPushButton("✗")
        button.setStyleSheet("background-color: #fb5454")
        button.setFont(QFont("Arial", 28, QFont.Medium))

        self.buttons.append(button)
        self.connect_button_to_slot(button)

        return button

    def change_button_properties(self):
        sender = self.sender()

        background_color = sender.styleSheet()
        index = background_color.index("background-color")
        background_color = background_color[index + 18:index+25]

        if background_color == "#60ff80":
            sender.setStyleSheet("background-color: #fb5454")
            sender.setText("✗")
        elif background_color == "#fb5454":
            sender.setStyleSheet("background-color: #60ff80")
            sender.setText("✓")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
