from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QSizePolicy, QVBoxLayout, QLabel, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QGraphicsEffect, QTextEdit,
                             QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF, QTimer, QDateTime, QDate, pyqtSignal, QUrl, QSize
from PyQt5.QtGui import QFont, QLinearGradient, QPainter, QBrush, QPen, QColor, QPixmap, QDesktopServices, QIcon
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from datetime import datetime
import json

# Change font sizes, colors, boldness, thickness.

# Create a function that returns the rgb properties of each widget type.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.buttons = []
        self.to_do_inputs = []
        self.date_completed_labels = []
        
        self.initUI()
        self.initJSON()
        self.init_button_and_to_do_input_properties()
        self.init_date_completed_label_properties()

    def initUI(self) -> None:
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
        self.setWindowIcon(QIcon("to_do_list.ico"))

        # Create title label.
        title_label = QLabel()
        title_label.setText("To-do List")
        title_label.setFont(QFont("Segoe Print", 30, QFont.Medium))
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

    def initJSON(self) -> None:
        """Initializes the JSON file with key value pairs for every to_do_input widget."""
        with open("to_do_list/to_do_list.json", "r+") as file:
            file_contents = file.read()

            if file_contents == "":
                data = {}

                for x in range(0, len(self.buttons)):
                    data[x] = {}
                    data[x]["text"] = ""
                    data[x]["completion_status"] = False
                    data[x]["date_completed"] = None

                file.write(json.dumps(data, indent=2))
                file.seek(0)

    def init_button_and_to_do_input_properties(self) -> None:
        """Initializes the properties of every button and to_do_input based on the "completion_status" of the respective to-do."""
        for x in range(0, len(self.buttons)):
            completion_status = self.get_completion_status(index=x)

            if completion_status == True:
                self.buttons[x].setText("✓") 
            elif completion_status == False:
                self.buttons[x].setText("✗") 

            to_do_input_stylesheet = self.get_to_do_input_style_sheet(completion_status)
            button_stylesheet = self.get_button_style_sheet(completion_status)
            self.to_do_inputs[x].setDisabled(completion_status)

            self.to_do_inputs[x].setStyleSheet(to_do_input_stylesheet)
            self.buttons[x].setStyleSheet(button_stylesheet)

    def init_date_completed_label_properties(self) -> None:
        """Initializes the properties of every date_completed_label based on the value of "date_completed" within the JSON file."""
        with open("to_do_list/to_do_list.json", "r") as file:
            file_contents = json.loads(file.read())
        
        for x in range(0, len(self.date_completed_labels)):
            date_completed = file_contents[str(x)]["date_completed"]

            if date_completed != None:
                self.date_completed_labels[x].setText(f"Completed on {date_completed}")

    def paintEvent(self, a0) -> None:
        """Creates and sets a gradiant background."""
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 0, Qt.SolidLine))

        gradiant = QLinearGradient(0, 0, 0, self.height())  # start at x1, y1, and end at x2, y2 
        gradiant.setColorAt(0, QColor("#aed1ef"))
        gradiant.setColorAt(0.5, QColor("#f2dfc1"))
        gradiant.setColorAt(1, QColor("#f0b9ef"))

        painter.setBrush(QBrush(gradiant))
        painter.drawRect(0, 0, self.width(), self.height())
    
    def get_to_do_input_text(self) -> dict:
        """
        Returns a dictionary consisting of information about every to-do if the JSON file is not empty.
        Returns an empty dictionary otherwise.
        """
        with open("to_do_list/to_do_list.json", "r") as file:
            file_contents = file.read()

        if file_contents == "":
            return {}
        else:
            return json.loads(file_contents)
        
    def get_completion_status(self, index: int) -> bool | None:
        """
        Gets the completion status of a to-do and returns it.
        
        :param index: An index position that determines which key in the dictionary to associate with.
        """
        with open("to_do_list/to_do_list.json", "r") as file:
            file_contents = json.loads(file.read())

        return file_contents[str(index)]["completion_status"]
    
    def get_button_style_sheet(self, is_complete: bool) -> str:
        """
        Returns a string consisting of the stylesheet for a QPushButton.
        
        :param is_complete: A boolean of if the button is marked as complete or not.
        """
        if is_complete == True:
            return f"""
                    QPushButton {{
                        background-color: rgba(255, 255, 255, 10);
                        color: grey;           
                        border: 1px solid;
                        border-color: grey;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(255, 255, 255, 75);  
                        color: grey;      
                        border-radius: 10px; 
                    }}
                    QPushButton:pressed {{
                        background-color: rgba(255, 255, 255, 255);
                        color: grey;       
                        border-radius: 10px;   
                    }}
                """
        elif is_complete == False:
            return f"""
                    QPushButton {{
                        background-color: rgba(255, 255, 255, 120);  
                        color: black;           
                        border: 1px solid;
                        border-color: grey;  
                    }}
                    QPushButton:hover {{
                        background-color: rgba(255, 255, 255, 200);  
                        color: black;         
                        border-radius: 10px;
                    }}
                    QPushButton:pressed {{
                        background-color: rgba(255, 255, 255, 255); 
                        color: black;      
                        border-radius: 10px;     
                    }}
                """
        
    def get_to_do_input_style_sheet(self, is_complete: bool) -> str:
        """
        Returns a string consisting of the stylesheet for a QLineEdit.
        
        :param is_complete: A boolean of if the to_do_input is marked as complete or not.
        """
        if is_complete == True:
            return "background-color: rgba(255, 255, 255, 10); color: grey; border: 1px solid rgb(122, 122, 122)"
        elif is_complete == False:
            return "background-color: rgba(255, 255, 255, 120); color: black; border: 1px solid rgb(122, 122, 122)"   

    def set_to_do_input_text(self) -> None:
        """Sets the text of each input field if the user has typed something into it previously."""
        input_text = self.get_to_do_input_text()

        try:
            for index, input in enumerate(self.to_do_inputs):
                input.setText(input_text[str(index)]["text"])
        except KeyError:
            pass

    def set_date_completed(self) -> None:
        """Sets the date a to-do was completed to a date_completed_label."""
        date = QDate.currentDate().toString()
            
        index = self.buttons.index(self.sender())
     
        date_completed_label = self.date_completed_labels[index]

        if date_completed_label.text() == "":
            date_completed_label.setText(f"Completed on {date}")
            self.save_date_completed_to_file(index=index, is_complete=True)
        else:
            date_completed_label.setText("")
            self.save_date_completed_to_file(index=index, is_complete=False)

    def change_button_properties(self) -> None:
        """
        Changes the properties of a button.
        Is called whenever a button is clicked.
        """
        button = self.sender()
        button_text = self.sender().text()

        if button_text == "✗":
            button.setText("✓") 
            rgb = self.get_button_style_sheet(True)
        elif button_text == "✓":
            button.setText("✗")
            rgb = self.get_button_style_sheet(False)
     
        button.setStyleSheet(rgb)
        self.change_to_do_input_properties(button)

    def change_to_do_input_properties(self, button: QPushButton) -> None:
        """
        Changes the properties of a to_do_input.
        Is called through self.change_button_properties whenever a button is clicked.
        
        :param button: A QPushButton widget.
        """
        index = self.buttons.index(self.sender())

        if button.text() == "✓":
            rgb = self.get_to_do_input_style_sheet(True)
            self.to_do_inputs[index].setDisabled(True)
        elif button.text() == "✗":
            rgb = self.get_to_do_input_style_sheet(False)
            self.to_do_inputs[index].setDisabled(False)

        self.to_do_inputs[index].setStyleSheet(rgb)

    def create_button(self) -> QPushButton:
            """Creates and returns a QPushButton that is used to set a to-do as completed."""
            button = QPushButton("✗")
            
            stylesheet = self.get_button_style_sheet(False)
            button.setStyleSheet(stylesheet)
            
            button.setFont(QFont("Segoe Print", 28, QFont.Medium))
            button.setFixedSize(69, 50)

            self.buttons.append(button)
            self.connect_button_to_slot(button)

            return button
    
    def create_to_do_input(self) -> QLineEdit:
        """Creates and returns a QLineEdit that is used for user input."""
        to_do_input = QLineEdit()
        to_do_input.setFont(QFont("Segoe UI", 15, QFont.Medium))

        rgb = self.get_to_do_input_style_sheet(False)
        to_do_input.setStyleSheet(rgb)
        

        to_do_input.setFixedSize(701, 51)

        self.to_do_inputs.append(to_do_input)
        self.connect_to_do_input_to_slot(to_do_input)

        return to_do_input
    
    def create_date_completed_label(self) -> QLabel:
        """Creates and returns a QLabel that is used to display the date in which a to-do is completed."""
        date_completed_label = QLabel()
        date_completed_label.setFont(QFont("Segoe Print", 10, QFont.Medium))
        date_completed_label.setAlignment(Qt.AlignRight)
        date_completed_label.setFixedSize(400, 39)
        self.date_completed_labels.append(date_completed_label)

        return date_completed_label

    def connect_button_to_slot(self, button: QPushButton) -> None:
        """
        Connects each button to various methods.
        Is called every time a button is created.
        
        :param button: A QPushButton widget.
        """
        button.clicked.connect(self.change_button_properties)
        button.clicked.connect(self.set_date_completed)
        button.clicked.connect(self.save_completion_status_to_file)

    def connect_to_do_input_to_slot(self, to_do_input: QLineEdit) -> None:
        """
        Connects each to_do_input to self.save_to_do_input_to_file to save their text to a JSON file whenever it changes.
        Is called every time a to_do_input is created.
        
        :param to_do_input: A QLineEdit widget.
        """
        to_do_input.textChanged.connect(self.save_to_do_input_to_file)

    def save_to_do_input_to_file(self) -> None:
        """Saves the text the user types to a JSON file."""
        with open("to_do_list/to_do_list.json", "r+") as file:
            file_contents = json.loads(file.read())
            file.seek(0)

            index_key = str(self.to_do_inputs.index(self.sender()))
            
            file_contents[index_key]["text"] = self.sender().text()
            file_contents = json.dumps(file_contents, indent=2)

            file.write(file_contents)
            file.truncate()

    def save_completion_status_to_file(self) -> None:
        """
        Saves the completion status of a to-do to a JSON file.
        Is called whenever a button is clicked.
        """
        with open("to_do_list/to_do_list.json", "r+") as file:
            file_contents = json.loads(file.read())
            file.seek(0)

            index_key = str(self.buttons.index(self.sender()))

            file_contents[index_key]["completion_status"] = not file_contents[index_key]["completion_status"] # Sets the completion status to the opposite boolean value.
            file_contents = json.dumps(file_contents, indent=2)
            file.write(file_contents)
            file.truncate()

    def save_date_completed_to_file(self, index: int, is_complete: bool) -> None:
        """
        Saves the date that a to-do was set as completed to a JSON file.
        Otherwise, it sets the date to None, and saves it to a JSON file.
        
        :param index: An index position that determines which date_completed_label in self.date_completed_labels to associate with.
        :param is_complete: A boolean that determines whether or not to save or delete the date completed.
        """
        with open("to_do_list/to_do_list.json", "r+") as file:
            file_contents = json.loads(file.read())
            file.seek(0)
            
            if is_complete == True:
                file_contents[str(index)]["date_completed"] = QDate.currentDate().toString()
            elif is_complete == False:
                file_contents[str(index)]["date_completed"] = None

            file_contents = json.dumps(file_contents, indent=2)
            file.write(file_contents)
            file.truncate()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()