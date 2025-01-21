from PySide6.QtWidgets import (
    QMainWindow, QLabel, QToolBar, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QSizePolicy, QToolButton
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from views.base_window import BaseWindow


class HomeWindow(BaseWindow):
    def __init__(self, controller):
        super(HomeWindow, self).__init__()
        self.controller = controller

        self.setWindowTitle("IsraFlight")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        # Set the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing
        central_widget.setLayout(layout)

        # Set the background label
        self.background_label = QLabel(self)
        pixmap = QPixmap("./israflightApp/images/back6-05.png")  # Replace with your image path
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        layout.addWidget(self.background_label)

        # Add the logo
        self.logo_below_text = QLabel(self.background_label)
        logo_pixmap = QPixmap("./israflightApp/images/israFlight_logo-03.png")  # Replace with your logo path
        self.logo_below_text.setPixmap(logo_pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Resize logo
        self.logo_below_text.move(120, 150)  # Position below the text

        # Overlay the text label
        self.text_label = QLabel(self.background_label)
        font = QFont("Urbanist", 12, QFont.Bold)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("color: #1C3664; margin-left: 20px;")  # Text color
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.resize(600, 150)  # Adjust height to fit multiple lines
        self.text_label.move(160, 370)  # Position the text label
        self.text_label.setText(
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit,\nsed diam nonummy nibh euismod tincidunt ut\nlaoreet dolore magna aliquam erat volutpat.\nUt wisi enim ad minim veniam, quis nostrud exerci\ntation ullamcorper suscipit lobortis nisl ut \naliquip ex ea commodo consequat."
        )

        # Add the form to the same layer
        self.form_widget = QWidget(self.background_label)
        self.form_widget.setGeometry(800, 250, 300, 200)  # left, top

        self.form_widget.setStyleSheet("""
                QWidget {
                    background-color: rgba(28, 54, 100, 0.8);  /* Semi-transparent dark background */
                    border-radius: 15px;                     /* Rounded corners */
                    padding: 15px;                           /* Padding inside the form */
                }                    
                                                  
                QLabel {
                    color: white;  /* Text color */
                    background: transparent;  /* Transparent background */
                    border: none;  /* No border */
                    font-family: 'Urbanist';       /* Font family */
                    font-size: 14px;              /* Font size */
                    font-weight: bold; 
                                      
                }
                QLineEdit {
                    background-color: white;
                    color: black;
                    border-radius: 5px;
                    padding: 5px;
                    font-family: 'Urbanist';       /* Font family */
                    font-size: 14px;              /* Font size */
                    font-weight: bold;                  
                }
                QPushButton {
                    background-color: #27AAE1;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-family: 'Urbanist';       /* Font family */
                    font-size: 14px;              /* Font size */
                    font-weight: bold;
                }
            """)

        # Make sure the layout and child widgets are not affected by the transparency
        self.form_widget.setAttribute(Qt.WA_StyledBackground, True)

        self.form_widget.resize(500, 350)

        # Create the form layout
        form_layout = QFormLayout(self.form_widget)
        form_layout.setContentsMargins(40, 30, 90, 5)  # Padding inside the form


        # Add a heading or description text to the form
        form_heading = QLabel("Sign In")
        form_heading.setFont(QFont("Urbanist", 18, QFont.Bold))
        form_heading.setStyleSheet("color: white;")  # Text color
        form_heading.setAlignment(Qt.AlignCenter)
        form_layout.addRow(form_heading)


        # Add fields to the form
        name_field = QLineEdit()
        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.Password)
        register_button = QPushButton("Sign In")
        register_button.clicked.connect(self.action1_triggered)

        
        form_layout.addRow("User Name:", name_field)
        form_layout.addRow("Password:", password_field)
        form_layout.addWidget(register_button)

        self.create_toolbar()
        #להוסיף עוד כפתור 


        #self.init_toolbar() 
        #אפשר למחוק את הקבצים של הtoolbar פה

    def init_toolbar(self):
        # Create a toolbar
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
        logo_pixmap = QPixmap("./israflightApp/images/israFlight_logo4-04.png")  # Replace with your logo path
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
        help_button.clicked.connect(self.action2_triggered)
        toolbar.addWidget(help_button)

        right_space = QWidget()
        right_space.setFixedWidth(60)  # Adjust spacing between buttons
        toolbar.addWidget(right_space)

    def action1_triggered(self):
        print("Action 1 triggered")

    def action2_triggered(self):
        print("Action 2 triggered")

    def resizeEvent(self, event):
        # Resize the background label
        if hasattr(self, 'background_label') and self.background_label:
            self.background_label.resize(self.size())
        super().resizeEvent(event)
