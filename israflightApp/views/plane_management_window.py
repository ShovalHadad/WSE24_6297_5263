from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QFileDialog, QSizePolicy, QMessageBox, QAbstractItemView
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from views.base_window import BaseWindow
from views.hover import HoverableTableWidget, HoverDelegate


class PlaneManagementWindow(BaseWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Plane Management")
        self.setGeometry(500, 200, 900, 600)
        self.setMinimumSize(900, 600)
        self.showMaximized()

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ------------------------ Right Side - Plane Table ------------------------
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(70, 50, 180, 50)
        right_layout.setSpacing(10)

        self.plane_list_title = QLabel("Plane List")
        self.plane_list_title.setFont(QFont("Urbanist", 18, QFont.Bold))
        self.plane_list_title.setAlignment(Qt.AlignCenter)
        self.plane_list_title.setFixedHeight(40)
        self.plane_list_title.setStyleSheet("""
            QLabel {
                color: #1C3664;
                background-color: #f3f3f3;
                padding: 10px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)
        right_layout.addWidget(self.plane_list_title)

        #self.plane_table = QTableWidget()
        self.plane_table = HoverableTableWidget()
        
        self.plane_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.plane_table.setColumnCount(4)
        self.plane_table.setHorizontalHeaderLabels(["    ID", "    Name", "    Made By", "    Year"])
    
        self.plane_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plane_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.plane_table.setFocusPolicy(Qt.NoFocus)
  
       # self.plane_table.setAlternatingRowColors(True)
        self.plane_table.setWordWrap(False)
        self.plane_table.setTextElideMode(Qt.ElideNone)

        delegate = HoverDelegate(self.plane_table)
        self.plane_table.setItemDelegate(delegate)
        self.plane_table.hover_index_changed.connect(delegate.on_hover_index_changed)
        self.plane_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #1C3664;
                border-radius: 10px;
                font-size: 14px;
                font-family: 'Urbanist';
                gridline-color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #1C3664;
                color: white;
                padding: 6px;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: #1C3664;
            }

           QTableWidget::item:hover {
                background-color: transparent;
            }
                                       
            /* SCROLLBAR DESIGN */
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.3);
                min-height: 30px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.5);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

        """)
        self.plane_table.verticalHeader().setVisible(False)
        self.plane_table.setShowGrid(False)
        self.plane_table.setAlternatingRowColors(False)
        self.plane_table.setColumnWidth(0, 120)
        self.plane_table.setColumnWidth(1, 250)
        self.plane_table.setColumnWidth(2, 200)
        self.plane_table.setColumnWidth(3, 150)

        right_layout.addWidget(self.plane_table)

        right_container = QWidget()
        right_container.setLayout(right_layout)
        right_container.setStyleSheet("background-color: none; border-radius: 20px;")
        right_container.setMinimumWidth(400)

        main_layout.addWidget(right_container, 2)

        # ------------------------ Left Side - Plane Form ------------------------
        self.add_plane_button = QPushButton("➕ Add Plane")
        self.add_plane_button.setFixedHeight(45)
        self.add_plane_button.setObjectName("addPlaneButton")
        self.add_plane_button.setStyleSheet("""
            QPushButton#addPlaneButton {
                background-color: #1C3664;
                color: white;
                border-radius: 20px;
                padding: 8px;
                font-size: 14px;
                width: 140px;
                border: none;
            }
            QPushButton#addPlaneButton:hover {
                background-color: #3A5A89;
            }
            QPushButton#addPlaneButton:pressed {
                background-color: #CDEBF6;
                border: none;
            }
        """)
        self.add_plane_button.clicked.connect(self.toggle_add_plane_form)

        self.form_widget = QWidget()
        self.form_widget.setFixedSize(580, 670)
        self.form_widget.setStyleSheet("""
            QWidget {
                background-color: #CDEBF6;
                border-radius: 20px;
                padding: 2px;
                border: none;
                margin-top: 25px;
                margin-bottom: 0px;
            }
        """)
        self.form_widget.hide()

        # ❌ Close Button
        self.close_form_button = QPushButton("✖")
        self.close_form_button.setFixedWidth(50)
        self.close_form_button.setFixedHeight(50)
        self.close_form_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        #self.close_form_button.setFixedSize(30, 30)
        self.close_form_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #1C3664;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.close_form_button.clicked.connect(self.close_form)

        self.form_layout = QVBoxLayout()
        self.form_widget.setLayout(self.form_layout)

        self.form_header = QLabel("ADD NEW PLANE")
        self.form_header.setAlignment(Qt.AlignCenter)
        self.form_header.setFixedHeight(60)
        self.form_header.setFont(QFont("Urbanist", 12, QFont.Bold))
        self.form_header.setStyleSheet("color: #123456; margin: 20px 0;")
        self.form_layout.addWidget(self.form_header)

        self.made_in_input = QLineEdit()
        self.nickname_input = QLineEdit()
        self.year_input = QLineEdit()

        self.picture_label = QLabel("Upload picture")
        self.picture_label.setAlignment(Qt.AlignCenter)
        self.picture_label.setFixedSize(100, 100)
        self.picture_label.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 10px;")

        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)

        def create_field(label_text, widget):
            container = QVBoxLayout()
            container.setSpacing(1) 
            
            label = QLabel(label_text)
            label.setFont(QFont("Urbanist", 12, QFont.Bold))
            label.setStyleSheet("""
                QLabel {
                    color: #123456;
                    padding-top: 5px;  
                    padding-bottom: 5px;  
                    font-size: 12px;
                    margin-left: 25px; 
                }
            """)
            widget.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 10px;
                    margin-top: 0px;
                    margin-bottom: 2px;  
                    margin-left: 25px; 
                    margin-right: 25px;                                      
                    color: black;
                    max-width: 500px;                   
                }
                QLineEdit::placeholder {
                    color: gray;
                }
            """)
            container.addWidget(label)
            container.addWidget(widget)
            return container

        self.form_layout.addLayout(create_field("Made In", self.made_in_input))
        self.form_layout.addLayout(create_field("Nickname", self.nickname_input))
        self.form_layout.addLayout(create_field("Year", self.year_input))
        self.form_layout.addWidget(self.picture_label, alignment=Qt.AlignCenter)
        self.form_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

        self.add_plane_submit = QPushButton("Add Plane")
        self.add_plane_submit.setFixedHeight(45)
        self.add_plane_submit.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 20px;
                padding: 8px;
                font-size: 14px;
                width: 140px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3A5A89;
            }
            QPushButton:pressed {
                background-color: #CDEBF6;
            }
        """)

        self.form_layout.addWidget(self.add_plane_submit, alignment=Qt.AlignCenter)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.add_plane_button, alignment=Qt.AlignCenter)
        left_layout.addWidget(self.form_widget)

        left_container = QWidget()
        left_container.setFixedSize(600, 700)
        left_container.setLayout(left_layout)
        #left_container.setFixedWidth(600)

        main_layout.addWidget(left_container, 1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.create_toolbar()

        self.load_planes()

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image")
        if file_path:
            pixmap = QPixmap(file_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.picture_label.setPixmap(pixmap)

    def load_planes(self):
        self.plane_table.setRowCount(0)
        planes = self.controller.get_planes()
        self.plane_table.setRowCount(len(planes))
        for row, plane in enumerate(planes):
            self.plane_table.setItem(row, 0, QTableWidgetItem("     " + str(plane.plane_id)))
            self.plane_table.setItem(row, 1, QTableWidgetItem("     " + plane.name))
            self.plane_table.setItem(row, 2, QTableWidgetItem("     " + plane.made_by))
            self.plane_table.setItem(row, 3, QTableWidgetItem("     " + str(plane.year)))

    def toggle_add_plane_form(self):
        if self.form_widget.isVisible():
            self.form_widget.hide()
            self.add_plane_button.show()
        else:
            self.reset_form_to_add_mode()
            self.form_widget.show()
            self.add_plane_button.hide()

    def close_form(self):
        self.form_widget.hide()
        self.add_plane_button.show()


    def reset_form_to_add_mode(self):
        """Resets the form to Add Plane mode (title, button, clear fields)."""
        self.form_header.setText("ADD NEW PLANE")
        self.add_plane_submit.setText("Add Plane")

        self.made_in_input.clear()
        self.nickname_input.clear()
        self.year_input.clear()
        self.picture_label.clear()
        self.picture_label.setText("Upload picture")
        self.picture_label.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 10px;")
        
        # נוודא שאין חיבורים כפולים
        try:
            self.add_plane_submit.clicked.disconnect()
        except TypeError:
            pass
        self.add_plane_submit.clicked.connect(self.controller.add_plane)  # שים לב להתאים את זה לפונקציה שלך בבקר



