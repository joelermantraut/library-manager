from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton,
                             QLineEdit, QMessageBox)
from PyQt6 import QtCore

from ManageDatabase import ManageBooksDatabase

class ModelWindow(QMainWindow):
    def __init__(self, db_manager: ManageBooksDatabase, title, styles: dict=None):
        super().__init__()

        self.db_manager = db_manager
        self.BOOKS_TABLE = "books"
        self.STUDENTS_TABLE = "students"
        self.PASSWORD_TABLE = "passwords"

        self.x = 100
        self.y = 100
        self.width = 500
        self.height = 200

        # Set window parameters
        self.setWindowTitle(title)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet("background-color: black")

        self.DEFAULT_STYLES = {
            "background-color": "black",
            "color": "white",
            "font": "bold 16px Timer New Roman",
            "border": "1px solid cyan",
            "padding": "10px"
        }
        self.styles = self.set_styles(self.DEFAULT_STYLES, styles)

    def set_styles(self, default_styles, styles):
        if not isinstance(styles, dict):
            return default_styles
            
        for style in styles.keys():
            if style in default_styles.keys():
                default_styles[style] = styles[style]
        # Replace new styles, and set others to default

        return default_styles
    
    def styles_string(self, styles):
        string = ";".join([f"{key}:{value}" for key, value in styles.items()])

        return string

    def show_info(self, title, message):
        QMessageBox.about(None, title, message)

    def add_label(self, text, styles=None):
        styles = self.set_styles(self.styles, styles)

        label = QLabel(text)
        label.setStyleSheet(self.styles_string(self.styles))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

        return label
    
    def add_button(self, text, command=None, styles=None):
        styles = self.set_styles(self.styles, styles)

        btn = QPushButton(text)
        btn.setStyleSheet(self.styles_string(self.styles))

        if command:
            btn.clicked.connect(command)

        return btn
    
    def add_line_edit(self, command=None, styles=None):
        styles = self.set_styles(self.styles, styles)

        line_edit = QLineEdit(self)
        line_edit.setStyleSheet(self.styles_string(self.styles))
        line_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        if command:
            line_edit.textChanged.connect(command)

        return line_edit