from PyQt6.QtWidgets import (QApplication, QVBoxLayout,
                             QGridLayout, QWidget, QFrame)

from ManageDatabase import ManageBooksDatabase
from ModelWindow import ModelWindow


class AdminMainWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.windows = list()
        self.title = title

        self.init_UI()

    def init_UI(self):
        title_label = self.add_label(self.title)
        old_pass_label = self.add_label("Current Password")
        self.old_pass_entry = self.add_line_edit()
        new_pass_label = self.add_label("New Password")
        self.new_pass_entry = self.add_line_edit()
        edit_pass_btn = self.add_button("Edit Admin Password", self.edit_pass)

        layout = QGridLayout()
        layout.addWidget(title_label, 0, 0, 1, 2)
        layout.addWidget(old_pass_label, 1, 0)
        layout.addWidget(self.old_pass_entry, 1, 1)
        layout.addWidget(new_pass_label, 2, 0)
        layout.addWidget(self.new_pass_entry, 2, 1)
        layout.addWidget(edit_pass_btn, 3, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        # Start with main window

    def edit_pass(self):
        old_pass = self.old_pass_entry.text()
        new_pass = self.new_pass_entry.text()
        db_pass = self.db_manager.get_property("passwords", "id", "1", "pass")
        if db_pass == old_pass:
            response = self.db_manager.edit("passwords", "id", "1", "pass", new_pass)

            if response:
                self.show_info("Change Password", "Password successfully change")
                self.old_pass_entry.setText("")
                self.new_pass_entry.setText("")
            else:
                self.show_info("Change Password", "Problem changing password")
        else:
            self.show_info("Change Password", "Current password not correct")

def main():
    app = QApplication([])

    with open(".credentials-books", "r") as file:
        content = file.read()
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()

    window = AdminMainWindow(manage_database, "Admin Manager")
    window.show()

    app.exec()

if __name__ == "__main__":
    main()