from PySide6.QtWidgets import QMainWindow, QToolBar, QLabel, QWidget, QToolButton, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class BaseWindow(QMainWindow):
    def __init__(self, controller=None):
        super(BaseWindow, self).__init__()
        self.controller = controller

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)

        toolbar.setStyleSheet("""
           QToolBar { 
              background-color: #1C3664; 
              color: white; 
              min-height: 50px; 
          }
          QToolButton {
              color: white;
              font-family: Urbanist;
              font-size: 15px;
          }
        """)

        left_space = QWidget()
        left_space.setFixedWidth(20)  # Adjust spacing between buttons
        toolbar.addWidget(left_space)

        # Add a logo to the toolbar
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("images/israFlight_logo4-04.png")  # Replace with your logo path
        logo_label.setPixmap(logo_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Resize logo
        toolbar.addWidget(logo_label)

        # Add a stretchable spacer to push buttons to the right
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(right_spacer)

        # Create "About Us" button
        about_us_button = QToolButton(self)
        about_us_button.setText("About Us")
        about_us_button.setToolTip("Learn more about us")
        toolbar.addWidget(about_us_button)

        # Add a small spacer between buttons
        button_spacer = QWidget()
        button_spacer.setFixedWidth(15)  # Adjust spacing between buttons
        toolbar.addWidget(button_spacer)

        # Create "Help" button
        help_button = QToolButton(self)
        help_button.setText("Help")
        help_button.setToolTip("Need help?")
        toolbar.addWidget(help_button)

        right_space = QWidget()
        right_space.setFixedWidth(60)  # Adjust spacing between buttons
        toolbar.addWidget(right_space)
