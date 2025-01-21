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

        # Main vertical layout to center the buttons
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the content vertically and horizontally
        central_widget.setLayout(layout)

        # Example content
        label = QLabel("Manager Main Page")
        label.setFont(QFont("Urbanist", 22, 700))
        label.setStyleSheet("""color: #27AAE1 """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)


        # Add a horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(25)  # Space between buttons


        # Add a spacer widget with fixed height
        spacer = QWidget()
        spacer.setFixedHeight(30)  # Adjust height as needed
        layout.addWidget(spacer)
        layout.addLayout(button_layout)

        # Button 1
        button1 = QPushButton("Flight Management")  # ניהול טיסות
        button1.setIcon(QIcon("./israflightApp/images/flight_managment.png"))  # Replace with your icon path
        button1.setFixedSize(250, 75)  # Resize the button
        button1.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 19px;              /* Font size */
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        button1.clicked.connect(self.add_flight_action)
        button_layout.addWidget(button1)

        # Button 2
        button2 = QPushButton("Add Manager")  # מינוי מנהל
        button2.setIcon(QIcon("./israflightApp/images/add_manager.png"))  # Replace with your icon path
        button2.setFixedSize(250, 75)  # Resize the button
        button2.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 19px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        button2.clicked.connect(self.edit_flight_action)
        button_layout.addWidget(button2)

        # Button 3
        button3 = QPushButton("Planes Management")
        button3.setIcon(QIcon("./israflightApp/images/planes_managment.png"))  # Replace with your icon path
        button3.setFixedSize(250, 75)  # Resize the button
        button3.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 20px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 19px;
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
