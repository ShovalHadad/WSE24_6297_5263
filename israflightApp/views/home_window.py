from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class HomeWindow(QMainWindow):
    def __init__(self, controller):
        super(HomeWindow, self).__init__()
        self.controller = controller

        self.setWindowTitle("IsraFlight - Home")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)

        # Main container
        container = QWidget()
        main_layout = QVBoxLayout(container)  # Use a QVBoxLayout for the main layout

        # Background image using QLabel
        self.background_label = QLabel()
        self.pixmap = QPixmap("./israflightApp/images/background.jpg")  # Make sure the path is correct
        self.background_label.setPixmap(self.pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.background_label)

        # Foreground widget with layout
        foreground_widget = QWidget()
        foreground_layout = QVBoxLayout(foreground_widget)

        # Add a semi-transparent overlay to the foreground widget
        foreground_widget.setStyleSheet("background: rgba(0, 0, 0, 0.7); border-radius: 10px;")  # Adjust opacity as needed

        # Label and button added to the foreground layout
        self.label = QLabel("Welcome to IsraFlight System!")
        self.label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold; margin: 20px;")
        self.label.setAlignment(Qt.AlignCenter)
        foreground_layout.addWidget(self.label)

        self.refresh_button = QPushButton("Refresh Data")
        self.refresh_button.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            margin: 10px;
        """)
        foreground_layout.addWidget(self.refresh_button)
        foreground_layout.setAlignment(Qt.AlignCenter)

        # Add the foreground widget to the main layout on top of the background image
        main_layout.addWidget(foreground_widget)

        # Set the main layout
        container.setLayout(main_layout)
        self.setCentralWidget(container)


