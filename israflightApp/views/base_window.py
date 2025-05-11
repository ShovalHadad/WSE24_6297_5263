from PySide6.QtWidgets import QMainWindow, QToolBar, QLabel, QWidget, QToolButton, QSizePolicy ,QStyle
from PySide6.QtGui import QPixmap , QIcon
from PySide6.QtCore import Qt ,QSize


class BaseWindow(QMainWindow):
    def __init__(self, controller=None, nav_controller=None):  # ✅ nav_controller נוסף כאן
        super(BaseWindow, self).__init__()
        self.controller = controller
        self.nav_controller = nav_controller  # ✅ שמירה של הנוויגציה

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
        left_space.setFixedWidth(20)
        toolbar.addWidget(left_space)

        logo_label = QLabel(self)
        logo_pixmap = QPixmap("./images/israFlight_logo4-04.png")
        #logo_pixmap = QPixmap("./israflightApp/images/israFlight_logo4-04.png")
        logo_label.setPixmap(logo_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        toolbar.addWidget(logo_label)

        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(right_spacer)

        # HOME Button
        home_button = QToolButton(self)
        home_button.setText("Home")
        home_button.setToolTip("Go back to the home page")
        toolbar.addWidget(home_button)
        spacer2 = QWidget()
        spacer2.setFixedWidth(30)
        toolbar.addWidget(spacer2)
       
        # ABOUT US Button
        about_us_button = QToolButton(self)
        about_us_button.setText("About Us")
        toolbar.addWidget(about_us_button)
        spacer3 = QWidget()
        spacer3.setFixedWidth(30)
        toolbar.addWidget(spacer3)


        # HELP Button
        help_button = QToolButton(self)
        help_button.setText("Help")
        toolbar.addWidget(help_button)
        spacer1 = QWidget()
        spacer1.setFixedWidth(30)
        toolbar.addWidget(spacer1)

    
        # BACK Button
        back_button = QToolButton(self)
        back_button.setIcon(QIcon("./images/back.png"))
        #back_button.setIcon(QIcon("./israflightApp/images/back.png"))
        back_button.setIconSize(QSize(30,30))  # גודל מותאם אישית
        #back_button.setText("Back")
        back_button.setToolTip("Go back to the previous page")
        toolbar.addWidget(back_button)

        right_space = QWidget()
        right_space.setFixedWidth(60)
        toolbar.addWidget(right_space)


        # ✅ חיבור הכפתורים לנוויגציה
        back_button.clicked.connect(self.go_back)
        home_button.clicked.connect(self.go_home)

    def go_back(self):
        """Go back to the previous page using the navigation controller."""
        if self.nav_controller:
            self.nav_controller.go_back()

    def go_home(self):
        """Go home directly using the navigation controller."""
        if self.nav_controller:
            self.nav_controller.go_home()
