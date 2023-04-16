from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QGridLayout, QLabel, QWidget, QPushButton,
                             QLineEdit, QMessageBox)
from PyQt6.QtCore import QCoreApplication

from ManageDatabase import ManageBooksDatabase

class ModelWindow(QMainWindow):
    def __init__(self, db_manager: ManageBooksDatabase, title, styles: dict=None):
        super().__init__()

        self.db_manager = db_manager

        self.x = 100
        self.y = 100
        self.width = 700
        self.height = 500

        # Set window parameters
        self.setWindowTitle(title)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet("background-color: black")

        self.DEFAULT_STYLES = {
            "background-color": "black",
            "color": "white",
            "font": "bold 20px Arial",
            "border": "1px solid cyan"
        }
        self.styles = self.set_styles(styles)

    def set_styles(self, styles):
        if not isinstance(styles, dict):
            return self.DEFAULT_STYLES
            
        default_styles = self.DEFAULT_STYLES
        for style in styles.keys():
            if style in default_styles.keys():
                default_styles[style] = styles[style]
        # Replace new styles, and set others to default

        return default_styles
    
    def styles_string(self):
        string = ";".join([f"{key}:{value}" for key, value in self.styles.items()])

        return string

    def show_info(self, title, message):
        QMessageBox.about(None, title, message)

    def add_label(self, text):
        label = QLabel(text)
        label.setStyleSheet(self.styles_string())

        return label
    
    def add_button(self, text, command=None):
        btn = QPushButton(text)
        btn.setStyleSheet(self.styles_string())

        if command:
            btn.clicked.connect(command)

        return btn
    
    def add_line_edit(self, command=None):
        line_edit = QLineEdit(self)
        line_edit.setStyleSheet("color: white;")

        if command:
            line_edit.textChanged.connect(command)

        return line_edit


class AddBookWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()
        book_ID_label = self.add_label("Book ID")
        book_title_label = self.add_label("Title")
        book_author_label = self.add_label("Author")
        book_status_label = self.add_label("Status")
        add_book_btn = self.add_button("Add Book", self.add_book)

        self.book_ID_entry = self.add_line_edit()
        self.book_title_entry = self.add_line_edit()
        self.book_author_entry = self.add_line_edit()
        self.book_status_entry = self.add_line_edit()

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(self.book_ID_entry, 0, 1)
        layout.addWidget(book_title_label, 1, 0)
        layout.addWidget(self.book_title_entry, 1, 1)
        layout.addWidget(book_author_label, 2, 0)
        layout.addWidget(self.book_author_entry, 2, 1)
        layout.addWidget(book_status_label, 3, 0)
        layout.addWidget(self.book_status_entry, 3, 1)
        layout.addWidget(add_book_btn, 4, 0)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def add_book(self):
        id = self.book_ID_entry.text()
        title = self.book_title_entry.text()
        author = self.book_author_entry.text()
        status = self.book_status_entry.text()

        response = self.db_manager.insert_book(id, title, author, status)
        if not response:
            # If response is False, is because book ID already exists
            self.db_manager.edit_book(id, "title", title)
            self.db_manager.edit_book(id, "author", author)
            response = self.db_manager.edit_book(id, "status", status)

            self.show_info("Book Added/Edited", "Failed on add or edit book")

        if response:
            # Command successfull
            self.show_info("Book Added/Edited", "Book successfully added or edited")


class ViewBooksWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout()

        self.filter_entry = self.add_line_edit(self.filter_entry_changed)
        self.list_books_label = self.add_label("books -----------------------------")

        layout.addWidget(self.filter_entry)
        layout.addWidget(self.list_books_label)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.list_books()

    def list_books(self):
        books_string = self.db_manager.list_books()
        self.list_books_label.setText(books_string)

    def filter_entry_changed(self):
        entry_text = self.filter_entry.text()

        books_string = self.db_manager.list_books().split("\n")

        for index, line in enumerate(books_string):
            pos = line.find(entry_text)
            if pos == -1:
                books_string.pop(index)

        self.list_books_label.setText("\n".join(books_string))


class RemoveBookWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()

        book_ID_label = self.add_label("Book ID")
        self.book_ID_entry = self.add_line_edit()
        issue_book_btn = self.add_button("Remove Book", self.remove_book)

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(self.book_ID_entry, 0, 1)
        layout.addWidget(issue_book_btn, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def remove_book(self):
        id = self.book_ID_entry.text()
        response = self.db_manager.delete_book(id)
        if response:
            self.show_info("Book deleted", "Book successfully deleted")
        else:
            self.show_info("Book deleted", "Failed on delete book")


class IssueBookWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()

        book_ID_label = self.add_label("Book ID")
        self.book_ID_entry = self.add_line_edit()
        issue_book_btn = self.add_button("Issue Book", self.issue_book)

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(self.book_ID_entry, 0, 1)
        layout.addWidget(issue_book_btn, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def issue_book(self):
        id = self.book_ID_entry.text()
        current_status = self.db_manager.get_property(id, "status")
        if current_status == "available":
            self.db_manager.edit_book(id, "status", "issued")

            self.show_info("Book issued", "Book successfully issued")
        else:
            self.show_info("Book issued", "Failed on issue book")


class ReturnBookWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()

        book_ID_label = self.add_label("Book ID")
        self.book_ID_entry = self.add_line_edit()
        return_book_btn = self.add_button("Return Book", self.return_book)

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(self.book_ID_entry, 0, 1)
        layout.addWidget(return_book_btn, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def return_book(self):
        id = self.book_ID_entry.text()
        current_status = self.db_manager.get_property(id, "status")
        if current_status == "issued":
            self.db_manager.edit_book(id, "status", "available")

            self.show_info("Return book", "Book successfully returned")
        else:
            self.show_info("Return book", "Failed on return book")


class MainWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        title_label = self.add_label("Library Manager")
        add_book_btn = self.add_button("Add/Edit Book", self.add_book)
        view_books_btn = self.add_button("View Books", self.view_books)
        issue_book_btn = self.add_button("Issue Book", self.issue_book)
        return_book_btn = self.add_button("Return Book", self.return_book)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(add_book_btn)
        layout.addWidget(view_books_btn)
        layout.addWidget(issue_book_btn)
        layout.addWidget(return_book_btn)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        # Start with main window

    def add_book(self):
        self.add_book_window = AddBookWindow(self.db_manager, "Add Book", self.styles)
        self.add_book_window.show()

    def remove_book(self):
        self.remove_book_window = RemoveBookWindow(self.db_manager, "Remove Book", self.styles)
        self.remove_book_window()

    def view_books(self):
        self.view_books_window = ViewBooksWindow(self.db_manager, "View Books", self.styles)
        self.view_books_window.show()

    def issue_book(self):
        self.issue_book_window = IssueBookWindow(self.db_manager, "Issue Book", self.styles)
        self.issue_book_window.show()

    def return_book(self):
        self.return_book_window = ReturnBookWindow(self.db_manager, "Return Book", self.styles)
        self.return_book_window.show()


def main():
    app = QApplication([])

    with open(".credentials", "r") as file:
        content = file.read()
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()

    window = MainWindow(manage_database, "Library Manager")
    window.show()

    app.exec()

if __name__ == "__main__":
    main()