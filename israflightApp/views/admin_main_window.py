from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from views.base_window import BaseWindow


class ManagerMainWindow(BaseWindow):
    def __init__(self, controller):
        super(ManagerMainWindow, self).__init__(controller)
        self.setWindowTitle("IsraFlight - Manager")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.create_toolbar()

        # Additional ManagerMainWindow-specific layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Example content
        label = QLabel("Welcome to IsraFlight Manager Page")
        label.setFont(QFont("Urbanist", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Add a horizontal layout for buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # Button 1
        button1 = QPushButton("Flight Management") #ניהול טיסות
        button1.setIcon(QIcon("./israflightApp/images/add_icon.png"))  # Replace with your icon path
        button1.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 14px;              /* Font size */
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        button1.clicked.connect(self.add_flight_action)
        button_layout.addWidget(button1)

        # Button 2
        button2 = QPushButton("Add Manager") #מינוי מנהל
        button2.setIcon(QIcon("./israflightApp/images/edit_icon.png"))  # Replace with your icon path
        button2.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        button2.clicked.connect(self.edit_flight_action)
        button_layout.addWidget(button2)

        # Button 3
        button3 = QPushButton("Airplanes Management")
        button3.setIcon(QIcon("./israflightApp/images/add_manager.png"))  # Replace with your icon path
        button3.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        button3.clicked.connect(self.delete_flight_action)
        button_layout.addWidget(button3)

    def add_flight_action(self):
        print("Add Flight button clicked!")

    def edit_flight_action(self):
        print("Edit Flight button clicked!")

    def delete_flight_action(self):
        print("Delete Flight button clicked!")
