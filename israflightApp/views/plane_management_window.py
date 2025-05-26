from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QFileDialog, QSizePolicy, QMessageBox, QAbstractItemView
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, Signal, QMetaObject
from views.base_window import BaseWindow
from views.hover import HoverableTableWidget, HoverDelegate
from base64 import b64encode
import requests



class ClickableLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()



class PlaneManagementWindow(BaseWindow):
    def __init__(self, controller, nav_controller=None):
        super().__init__(controller=controller, nav_controller=nav_controller)
        self.controller = controller

        self.setWindowTitle("Plane Management")
        self.setGeometry(500, 200, 900, 600)
        self.setMinimumSize(900, 600)
        self.showMaximized()

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Left, Top, Right, Bottom
        main_layout.setSpacing(20)  # Space between table and form


        # ------------------------ Right Side - Plane Table ------------------------
        self.selected_plane_id = None

        right_layout = QVBoxLayout()
        #right_layout.setContentsMargins(70, 50, 180, 50)
        right_layout.setContentsMargins(90, 50, 60, 50)

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

        self.plane_table.itemClicked.connect(self.handle_plane_table_double_click)


        right_layout.addWidget(self.plane_table)
        right_container = QWidget()
        right_container.setLayout(right_layout)
        right_container.setStyleSheet("background-color: none; border-radius: 20px;")
        right_container.setMinimumWidth(100)

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
        self.form_layout.setContentsMargins(20, 20, 20, 20)
        self.form_layout.setSpacing(3)

        self.form_widget.setLayout(self.form_layout)
        self.form_layout.addWidget(self.close_form_button, alignment=Qt.AlignLeft)

        header_container = QVBoxLayout()
        header_container.setContentsMargins(0, 20, 0, 0)  # Top margin = 20

        self.form_header = QLabel("ADD NEW PLANE")
        self.form_header.setAlignment(Qt.AlignCenter)
        self.form_header.setFixedHeight(60)
        self.form_header.setFont(QFont("Urbanist", 12, QFont.Bold))
        self.form_header.setStyleSheet("color: #123456;")
        header_container.addWidget(self.form_header)

        self.form_layout.addLayout(header_container)

        self.made_in_input = QLineEdit()
        self.nickname_input = QLineEdit()
        self.year_input = QLineEdit()

        self.picture_label = ClickableLabel("Upload picture")
        self.picture_label.setAlignment(Qt.AlignCenter)
        self.picture_label.setFixedSize(100, 100)
        self.picture_label.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 10px; margin:3px;")
        self.picture_label.clicked.connect(self.upload_image)


        def create_field(label_text, widget):
            container = QVBoxLayout()
            container.setSpacing(1) 
            
            label = QLabel(label_text)
            label.setFont(QFont("Urbanist", 12, QFont.Bold))
            label.setStyleSheet("""
                QLabel {
                    color: #123456;
                    padding-top: 5px;  
                    padding-bottom: 0px;  
                    font-size: 14px;
                    margin-left: 25px; 
                }
            """)
            widget.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 12px;
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
        



        # 💾 Save add plane Button
        self.save_plane_button = QPushButton("Save Plane")
        self.save_plane_button.setFixedHeight(80)
        self.save_plane_button.setFixedWidth(140)  # Adjust width as needed
        self.save_plane_button.setObjectName("saveButton")
        self.save_plane_button.setStyleSheet("""
            QPushButton#saveButton {
                background-color: #1C3664;
                color: white;
                border-radius: 20px;
                padding: 8px;
                margin-bottom: 10px;                      
                font-size: 14px;
                border: none;
            }
            QPushButton#saveButton:hover {
                background-color: #3A5A89;
            }
            QPushButton#saveButton:pressed {
                background-color: #0D253F;
            }
        """)
        self.save_plane_button.clicked.connect(self.save_plane)

        # 🗑️ Delete Button
        self.delete_button = QPushButton("Delete Plane")
        self.delete_button.setFixedHeight(80)
        self.delete_button.setFixedWidth(140)  # Adjust width as needed
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.setStyleSheet("""
            QPushButton#deleteButton {
                background-color: #D32F2F;
                color: white;
                border-radius: 20px;
                padding: 8px;
                margin-bottom: 10px;                      
                font-size: 14px;
                border: none;
            }
            QPushButton#deleteButton:hover {
                background-color: #B71C1C;
            }
            QPushButton#deleteButton:pressed {
                background-color: #7F0000;
            }
        """)
        #self.delete_button.clicked.connect(self.delete_selected_flight)
        self.delete_button.hide()  # Hide by default

        self.save_plane_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_row = QHBoxLayout()
        button_row.setSpacing(4)  # רווח בין הכפתורים
        button_row.setContentsMargins(0, 0, 0, 0)  # ביטול שוליים פנימיים
        button_row.addWidget(self.save_plane_button)
        button_row.addWidget(self.delete_button)
        self.form_layout.addLayout(button_row)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.add_plane_button, alignment=Qt.AlignCenter)
        left_layout.addWidget(self.form_widget)

        left_container = QWidget()
        left_container.setFixedSize(700, 700)
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
            self.picture_path = file_path  # לשימוש ב-update או add

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
        self.save_plane_button.setText("Save Plane")

        self.made_in_input.clear()
        self.nickname_input.clear()
        self.year_input.clear()
        self.picture_label.clear()
        self.picture_label.setText("Upload picture")
        self.picture_label.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 10px;
            color: #888;
        """)
        
        try:
            self.save_plane_button.clicked.disconnect()
        except TypeError:
            pass
        self.save_plane_button.clicked.connect(self.save_plane)



    def encode_image_to_base64(self, file_path):
        try:
            with open(file_path, "rb") as image_file:
                return b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            print(f"Error encoding image: {e}")
            return ""

    
    def upload_to_imgur(self, image_path, client_id):
        headers = {"Authorization": f"Client-ID {client_id}"}
        with open(image_path, "rb") as image_file:
            data = {"image": image_file.read()}
            response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=data)
        if response.status_code == 200:
            return response.json()["data"]["link"]
        else:
            raise Exception(f"Upload failed: {response.status_code} - {response.text}")


       

    def save_plane(self):
        picture_path = getattr(self, "picture_path", "")
        try:
            if picture_path:
                imgur_url = self.upload_to_imgur(picture_path, "8a1ceabf164ec32")

            else:
                imgur_url = ""

            plane_data = {
                "Name": self.nickname_input.text(),
                "MadeBy": self.made_in_input.text(),
                "Year": self.year_input.text(),
                "Picture": imgur_url,
                "NumOfSeats1": 20,
                "NumOfSeats2": 50,
                "NumOfSeats3": 100,
            }

            success = self.controller.add_plane(plane_data)
            if success:
                self.load_planes()
                QMessageBox.information(self, "Success", "Plane added successfully ✅")
                self.form_widget.hide()
                self.add_plane_button.show()
            else:
                QMessageBox.warning(self, "Error", "⚠️ there is no plane in the picture.")

        except Exception as e:
            QMessageBox.critical(self, "Upload Error", str(e))



    def delete_plane(self, plane_id):
        confirm = QMessageBox.question(
            self,
            "Delete Plane",
            "Are you sure you want to delete this plane?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            success = self.controller.delete_plane(plane_id)
            if success:
                self.load_planes()
                QMessageBox.information(self, "Success", "Plane deleted successfully 🗑️")
                self.close_form()
            else:
                QMessageBox.warning(self, "Error", "⚠️ Failed to delete plane. please call IT.")




    def edit_plane(self, plane):
        self.selected_plane_id = plane.plane_id

        self.form_header.setText("EDIT PLANE")
        self.save_plane_button.setText("Update Plane")
        self.form_widget.show()
        self.add_plane_button.hide()

        self.made_in_input.setText(plane.made_by)
        self.nickname_input.setText(plane.name)
        self.year_input.setText(str(plane.year))
        self.picture_label.clear()
        self.picture_label.setText("Current image")

        # ✨ כאן מנתקים את הפעולה הקודמת של הכפתור
        try:
            self.save_plane_button.clicked.disconnect()
        except TypeError:
            pass

        # ✨ ואז מחברים את כפתור השמירה לפונקציית העדכון
        self.save_plane_button.clicked.connect(self.update_plane)

        try:
            self.delete_button.clicked.disconnect()
        except TypeError:
            pass
        self.delete_button.clicked.connect(lambda: self.delete_plane(plane.plane_id))
        self.delete_button.show()



    def disconnect_all_slots(signal):
        try:
            while signal.disconnect():
                pass
        except Exception:
            pass



    def handle_plane_table_double_click(self):
        selected_row = self.plane_table.currentRow()
        if selected_row >= 0:
            plane_id_item = self.plane_table.item(selected_row, 0)
            plane_id = int(plane_id_item.text().strip())
            plane = self.controller.get_plane_by_id(plane_id)
            if plane:
                self.edit_plane(plane)


    def update_plane(self):
        """Updates an existing plane via the controller."""
        if not self.selected_plane_id:
            print("No Plane Selected, No plane selected for update.")
            return

        plane_data = {
            "PlaneId": self.selected_plane_id,
            "Name": self.nickname_input.text(),
            "MadeBy": self.made_in_input.text(),
            "Year": self.year_input.text(),
            "Picture": self.picture_label.pixmap(),  # or path/base64 depending on how you handle it
            # add NumOfSeats if applicable
        }

        success = self.controller.update_plane(plane_data)
        if success:
            self.load_planes()
            QMessageBox.information(self, "Success", "Plane updated successfully ✈️")
            self.close_form()
        else:
            QMessageBox.warning(self, "Error", "⚠️ Failed to update plane. piease call IT.")


    
