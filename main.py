from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QWidget)
from ManageDatabase import ManageBooksDatabase

from ModelWindow import ModelWindow
from BooksMainWindow import BooksMainWindow
from StudentsMainWindow import StudentsMainWindow
from AdminWindow import AdminMainWindow

class MainWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.windows = list()
        self.title = title

        self.init_UI()

    def init_UI(self):
        title_label = self.add_label(self.title)
        books_manager_btn = self.add_button("Open Books Manager", self.open_books_manager)
        students_manager_btn = self.add_button("Open Students Manager", self.open_students_manager)
        admin_manager_btn = self.add_button("Open Admin Manager", self.open_admin_manager)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(books_manager_btn)
        layout.addWidget(students_manager_btn)
        layout.addWidget(admin_manager_btn)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        # Start with main window

    def open_books_manager(self):
        self.books_window = BooksMainWindow(self.db_manager, "Books Manager", "books")
        self.open_window_if_not_other_opened(self.books_window)

    def open_students_manager(self):
        self.students_window = StudentsMainWindow(self.db_manager, "Students Manager", "students")
        self.open_window_if_not_other_opened(self.students_window)

    def open_admin_manager(self):
        self.admin_window = AdminMainWindow(self.db_manager, "Admin Manager", "passwords")
        self.open_window_if_not_other_opened(self.admin_window)

def main():
    app = QApplication([])

    with open(".credentials-books", "r") as file:
        content = file.read()[0:-1]
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()

    window = MainWindow(manage_database, "Library Manager")
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
