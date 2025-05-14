from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QToolButton
from PySide6.QtGui import QFont, QIcon, QPixmap, QResizeEvent
from PySide6.QtCore import Qt, QSize
from views.base_window import BaseWindow
from PySide6.QtGui import QGuiApplication



class ManagerMainWindow(BaseWindow):
    def __init__(self, controller, flyer_id, nav_controller=None):
        super().__init__(controller=controller, nav_controller=nav_controller)
        self.controller = controller
        screen = QGuiApplication.primaryScreen()

        self.setWindowTitle("IsraFlight - Manager")
        self.setGeometry(screen.geometry())
        self.setMinimumSize(800, 600)
        self.showMaximized()

        # --- Central widget ---
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.create_toolbar()

        # ✅ BACKGROUND QLabel (הכי חשוב)
        self.background_label = QLabel(central_widget)
        #self.background_pixmap = QPixmap("./israflightApp/images/manager_background.png")
       # self.background_label.setPixmap(self.background_pixmap)
        #self.background_label.setScaledContents(True)  # כדי שהתמונה תתפרס אוטומטית

        # ✅ MAIN LAYOUT
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignCenter)

        # Label (Title)
        label = QLabel()
        label.setFont(QFont("Urbanist", 22, 700))
        label.setStyleSheet("""color: #27AAE1""")
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        # Horizontal layout for the 2 circular buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(50)
        main_layout.addLayout(self.button_layout)

        # Add buttons (connections will be initialized later)
        self.create_buttons(main_layout, flyer_id)

    def resizeEvent(self, event: QResizeEvent):
        """Update background size when window is resized"""
        # ✅ הגנה כדי לא לקרוס במקרה מוזר
        if hasattr(self, 'background_label') and self.background_label:
            self.background_label.resize(self.size())
        super().resizeEvent(event)

    def create_buttons(self, main_layout, flyer_id):
        # --- LEFT SIDE: Flight Management ---

        # Left Container
        left_container = QWidget()
        left_container.setStyleSheet("""
            background-color: #F9F9F9;  /* צבע רקע */
            border-radius: 20px;
        """)
        left_layout = QVBoxLayout(left_container)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(20, 20, 20, 20)  # קצת רווח פנימי
        left_layout.setSpacing(30)  # 🆕 רווח בין כל אלמנט

        # Icon
        self.button1_icon = QLabel()
        self.button1_icon.setPixmap(QPixmap("./images/f_managment.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #self.button1_icon.setPixmap(QPixmap("./israflightApp/images/f_managment.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.button1_icon.setStyleSheet("margin-left: 130px;")
        left_layout.addWidget(self.button1_icon)

        # Button
        self.button1 = QPushButton("Flights Management")
        self.button1.setFixedSize(250, 43)
        self.button1.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                font-family: 'Urbanist';
                font-size: 16px;
                margin-left: 75px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        left_layout.addWidget(self.button1)

        # Description Text
        desc1 = QLabel("Manage all flights: schedule, edit, and view details.")
        desc1.setWordWrap(True)
        desc1.setAlignment(Qt.AlignCenter)
        desc1.setFont(QFont("Urbanist", 12))
        left_layout.addWidget(desc1)

        # Additional Text for left side
        extra_desc1 = QLabel("Track flight statuses in real-time, cancel or reschedule flights, and get updates about delays and gate changes.")
        extra_desc1.setWordWrap(True)
        extra_desc1.setAlignment(Qt.AlignCenter)
        extra_desc1.setFont(QFont("Urbanist", 12))
        extra_desc1.setStyleSheet("color: #555555;")
        left_layout.addWidget(extra_desc1)

        # --- RIGHT SIDE: Planes Management ---

        # Right Container
        right_container = QWidget()
        right_container.setStyleSheet("""
            background-color: #F9F9F9;  /* צבע רקע */
            border-radius: 20px;
            margin-right:100px;
        """)
        right_layout = QVBoxLayout(right_container)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(50, 20, 50, 20)
        right_layout.setSpacing(30)  # 🆕 רווח בין כל אלמנט

        # Icon
        self.button3_icon = QLabel()
        self.button3_icon.setPixmap(QPixmap("./images/p_managment.png").scaled(65, 65, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #self.button3_icon.setPixmap(QPixmap("./israflightApp/images/p_managment.png").scaled(65, 65, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.button3_icon.setStyleSheet("margin-left: 130px;")
        right_layout.addWidget(self.button3_icon)

        # Button
        self.button3 = QPushButton("Planes Management")
        self.button3.setFixedSize(350, 43)
        self.button3.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                font-family: 'Urbanist';
                font-size: 16px;
                margin-left: 70px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        right_layout.addWidget(self.button3)

        # Description Text
        desc3 = QLabel("Manage aircraft details: add, update, and verify planes.")
        desc3.setWordWrap(True)
        desc3.setAlignment(Qt.AlignCenter)
        desc3.setFont(QFont("Urbanist", 12))
        right_layout.addWidget(desc3)

        # Additional Text for right side
        extra_desc3 = QLabel("Maintain detailed logs of aircraft maintenance, schedule technical checks, and ensure compliance with aviation safety standards.")
        extra_desc3.setWordWrap(True)
        extra_desc3.setAlignment(Qt.AlignCenter)
        extra_desc3.setFont(QFont("Urbanist", 12))
        extra_desc3.setStyleSheet("color: #555555;")
        right_layout.addWidget(extra_desc3)

        # --- MIDDLE: Separator Line ---
        line = QLabel()
        line.setFixedWidth(2)
        line.setStyleSheet("background-color: #D9D9D9;")
        line.setMinimumHeight(550)

        # --- COMBINE LEFT + LINE + RIGHT ---
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(100)
        middle_layout.setAlignment(Qt.AlignCenter)
        middle_layout.addWidget(left_container)
        middle_layout.addWidget(line)
        middle_layout.addWidget(right_container)

        main_layout.addLayout(middle_layout)

        # --- BACK BUTTON BELOW ---
        self.back_button = QPushButton("Go to Frequent Flyer")
        self.back_button.setFixedSize(450, 75)
        self.back_button.setStyleSheet("""
            QPushButton {
                margin-right: 120px;
                color: #27AAE1;
                border-radius: 15px;
                font-family: 'Urbanist';
                font-size: 19px;
            }
            QPushButton:hover {
                color: #125E80;
            }
        """)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

    def initialize_controller(self, controller, flyer_id):
        self.controller = controller
        self.button1.clicked.connect(self.controller.open_flight_management)
        self.button3.clicked.connect(self.controller.open_planes_management)
        self.back_button.clicked.connect(lambda: self.controller.back_to_frequent_flyer(flyer_id))
