from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QScrollArea, QHBoxLayout, QPushButton, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from views.base_window import BaseWindow


class AddManagerWindow(BaseWindow):
    def __init__(self, controller):
        super().__init__()
        #self.base_url = base_url  # API base URL
        self.controller = controller

        self.setWindowTitle("Add Manager")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.create_toolbar()

        # Fetch frequent flyers from the API
        #self.frequent_flyers = self.controller.get_all_flyers(self.base_url)
        #self.filtered_flyers = self.frequent_flyers  # For search functionality

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Search area
        search_label = QLabel("Search Employee:")
        search_label.setFont(QFont("Urbanist", 14))
        layout.addWidget(search_label)

 
    