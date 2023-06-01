from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton,
                             QLineEdit, QMessageBox, QInputDialog)
from PyQt6 import QtCore

from ManageDatabase import ManageBooksDatabase

class ModelWindow(QMainWindow):
    def __init__(self, db_manager: ManageBooksDatabase, title, table, styles: dict=None):
        super().__init__()

        self.db_manager = db_manager
        self.table = table

        self.x = 100
        self.y = 100
        self.width = 500
        self.height = 200

        self.windows = list()

        # Set window parameters
        self.setWindowTitle(title)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet("""
            QInputDialog *{color: white;border: 1px solid white;padding: .5em;};
            background-color: black;
        """)

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
        
        default_styles = default_styles.copy()

        for style in styles.keys():
            default_styles[style] = styles[style]
        # Replace new styles, and set others to default

        return default_styles
    
    def styles_string(self, styles):
        string = ";".join([f"{key}:{value}" for key, value in styles.items()])

        return string

    def show_info(self, title, message):
        QMessageBox.about(None, title, message)

    def run_password_manager(self):
        qinputdialog = QInputDialog()
        password, ok = qinputdialog.getText(self, "Password input", "Password: ", QLineEdit.EchoMode.Password)
        if ok:
            return password
        return None

    def add_label(self, text, styles=None):
        styles = {"border": "none", "border-left": "3px solid teal", "border-bottom": "3px solid teal"}
        styles = self.set_styles(self.styles, styles)

        label = QLabel(text)
        label.setStyleSheet(self.styles_string(styles))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        return label
    
    def add_button(self, text, command=None, styles=None):
        styles = self.set_styles(self.styles, styles)

        btn = QPushButton(text)
        btn.setStyleSheet(self.styles_string(styles))

        if command:
            btn.clicked.connect(command)

        return btn
    
    def add_line_edit(self, command=None, styles=None):
        styles = {"border": "none", "border-bottom": "2px dotted teal"}
        styles = self.set_styles(self.styles, styles)

        line_edit = QLineEdit(self)
        line_edit.setStyleSheet(self.styles_string(styles))
        line_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        if command:
            line_edit.textChanged.connect(command)

        return line_edit

    def open_window_if_not_other_opened(self, window):
        for w in self.windows:
            if w and w != window and w.isVisible():
                return False

        if not window in self.windows:
            self.windows.append(window)

        window.show()
