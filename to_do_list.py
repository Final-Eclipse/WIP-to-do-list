from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QSizePolicy, QVBoxLayout, QLabel, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QGraphicsEffect, QTextEdit,
                             QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF, QTimer, QDateTime, QDate, pyqtSignal, QUrl, QSize
from PyQt5.QtGui import QFont, QLinearGradient, QPainter, QBrush, QPen, QColor, QPixmap, QDesktopServices
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from datetime import datetime

# Dynamically create to-dos.
# Create add and remove to-do buttons.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.to_do_button.clicked.connect(self.change_button_properties)

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
        # self.todos_area_layout.setSpacing(0)
        self.todos_area_widget.setStyleSheet("background-color: #e6fd93")
        main_layout.addWidget(self.todos_area_widget, 1, 0, 1, 2)

        # Create buttons for to-dos.
        self.to_do_button = QPushButton("✗")
        self.to_do_button.setStyleSheet("background-color: #fb5454")
        self.to_do_button.setFont(QFont("Arial", 30, QFont.Medium))
        self.todos_area_layout.addWidget(self.to_do_button, 0, 0, 1, 1)

        # Create to-do text area.
        self.to_do_text = QLineEdit()
        self.to_do_text.setStyleSheet("background-color: #60ffcf")
        self.to_do_text.setFont(QFont("Arial", 30, QFont.Medium))
        self.todos_area_layout.addWidget(self.to_do_text, 0, 1, 1, 10)

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
