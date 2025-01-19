from PySide6.QtWidgets import QMainWindow, QLabel, QToolBar, QWidget, QVBoxLayout, QGraphicsOpacityEffect, QSizePolicy, QToolButton
from PySide6.QtGui import QPixmap, QAction, QFont
from PySide6.QtCore import Qt

class HomeWindow(QMainWindow):
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

       # Set the background label with transparency
        self.background_label = QLabel(self)
        pixmap = QPixmap("./israflightApp/images/background.jpg")  # Replace with your image path
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)

        # Apply transparency effect
        #opacity_effect = QGraphicsOpacityEffect(self.background_label)
        #opacity_effect.setOpacity(0.5)  # Set opacity level (0.0 is fully transparent, 1.0 is fully opaque)
        #self.background_label.setGraphicsEffect(opacity_effect)

        # Add the background label to the layout
        layout.addWidget(self.background_label)
        

        # Overlay the text label
        self.text_label = QLabel("Your Text Here", self.background_label)
        font = QFont("Urbanist", 20, QFont.Bold)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("color: white; margin-left: 20px;")  # Text color
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.text_label.resize(600, 50)  # Set size of the text label
        self.text_label.move(20, 20)  # Position the text label


         # Add the logo below the text
        self.logo_below_text = QLabel(self.background_label)
        logo_pixmap = QPixmap("./israflightApp/images/israFlight_logo-03.png")  # Replace with your logo path
        self.logo_below_text.setPixmap(logo_pixmap.scaled(550, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Resize logo
        self.logo_below_text.move(80, 150)  # Adjust the position below the text label

        self.init_toolbar()



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
        about_us_button.clicked.connect(self.action1_triggered)
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
