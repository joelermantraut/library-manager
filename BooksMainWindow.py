from PyQt6.QtWidgets import (QApplication, QVBoxLayout,
                             QGridLayout, QWidget, QFrame)

from ManageDatabase import ManageBooksDatabase
from ModelWindow import ModelWindow


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
        layout.addWidget(add_book_btn, 4, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def add_book(self):
        id = self.book_ID_entry.text()
        title = self.book_title_entry.text()
        author = self.book_author_entry.text()
        status = self.book_status_entry.text()

        response = self.db_manager.insert(self.BOOKS_TABLE, {"bid": id, "title": title, "author": author, "status": status})
        if not response:
            # If response is False, is because book ID already exists
            self.db_manager.edit(self.BOOKS_TABLE, "bid", id, "title", title)
            self.db_manager.edit(self.BOOKS_TABLE, "bid", id, "author", author)
            response = self.db_manager.edit(self.BOOKS_TABLE, "bid", id, "status", status)

            if not response:
                self.show_info("Book Added/Edited", "Failed on add or edit book")
            else:
                self.show_info("Book Added/Edited", "Successfully edited book")

        if response:
            self.show_info("Book Added/Edited", "Book successfully added")


class ViewBooksWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout()

        self.filter_entry = self.add_line_edit(self.filter_entry_changed)
        self.list_books_label = self.add_label("", {"font": "bold 11px Arial"})

        layout.addWidget(self.filter_entry)
        layout.addWidget(self.list_books_label)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.list_books()

    def list_books(self):
        books_string = "BID\t\tTitle\t\tAuthor\t\tStatus\n"
        books_string += self.db_manager.list(self.BOOKS_TABLE)
        self.list_books_label.setText(books_string)

    def filter_entry_changed(self):
        entry_text = self.filter_entry.text()

        books_string = self.db_manager.list(self.BOOKS_TABLE).split("\n")

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
        remove_book_btn = self.add_button("Remove Book", self.remove_book)

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(self.book_ID_entry, 0, 1)
        layout.addWidget(remove_book_btn, 1, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def remove_book(self):
        id = self.book_ID_entry.text()
        response = self.db_manager.delete(self.BOOKS_TABLE, "bid", id)
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
        student_file_label = self.add_label("Student file")
        self.student_file_entry = self.add_line_edit()
        issue_book_btn = self.add_button("Issue Book", self.issue_book)

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(self.book_ID_entry, 0, 1)
        layout.addWidget(student_file_label, 1, 0)
        layout.addWidget(self.student_file_entry, 1, 1)
        layout.addWidget(issue_book_btn, 2, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def issue_book(self):
        id = self.book_ID_entry.text()
        file = self.student_file_entry.text()
        current_status = self.db_manager.get_property(self.BOOKS_TABLE, "bid", id, "status")
        if current_status == "available":
            self.db_manager.edit(self.BOOKS_TABLE, "bid", id, "status", "issued")

            self.db_manager.insert(f"student{file}", {"bid": id, "issue_date": "2023-04-20", "return_date": "2023-05-20"})
            # Inserts book issued in students table

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
        layout.addWidget(return_book_btn, 1, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def return_book(self):
        id = self.book_ID_entry.text()
        current_status = self.db_manager.get_property(self.BOOKS_TABLE, "bid", id, "status")
        if current_status == "issued":
            self.db_manager.edit(self.BOOKS_TABLE, "bid", id, "status", "available")

            self.show_info("Return book", "Book successfully returned")
        else:
            self.show_info("Return book", "Failed on return book")


class BooksMainWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.windows = list()
        self.title = title

        self.init_UI()

    def init_UI(self):
        title_label = self.add_label(self.title)
        add_book_btn = self.add_button("Add/Edit Book", self.add_book)
        remote_book_btn = self.add_button("Remove Book", self.remove_book)
        view_books_btn = self.add_button("View Books", self.view_books)
        issue_book_btn = self.add_button("Issue Book", self.issue_book)
        return_book_btn = self.add_button("Return Book", self.return_book)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.VLine)
        frame.setFrameShadow(QFrame.Shadow.Sunken)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(frame)
        layout.addWidget(add_book_btn)
        layout.addWidget(remote_book_btn)
        layout.addWidget(view_books_btn)
        layout.addWidget(issue_book_btn)
        layout.addWidget(return_book_btn)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        # Start with main window

    def open_window_if_not_other_opened(self, window):
        for w in self.windows:
            if w and w != window and w.isVisible():
                return False

        if not window in self.windows:
            self.windows.append(window)

        window.show()

    def add_book(self):
        self.add_book_window = AddBookWindow(self.db_manager, "Add Book", self.styles)
        self.open_window_if_not_other_opened(self.add_book_window)

    def remove_book(self):
        self.remove_book_window = RemoveBookWindow(self.db_manager, "Remove Book", self.styles)
        self.open_window_if_not_other_opened(self.remove_book_window)

    def view_books(self):
        self.view_books_window = ViewBooksWindow(self.db_manager, "View Books", self.styles)
        self.open_window_if_not_other_opened(self.view_books_window)

    def issue_book(self):
        self.issue_book_window = IssueBookWindow(self.db_manager, "Issue Book", self.styles)
        self.open_window_if_not_other_opened(self.issue_book_window)

    def return_book(self):
        self.return_book_window = ReturnBookWindow(self.db_manager, "Return Book", self.styles)
        self.open_window_if_not_other_opened(self.return_book_window)


def main():
    app = QApplication([])

    with open(".credentials-books", "r") as file:
        content = file.read()
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()

    window = BooksMainWindow(manage_database, "Books Manager")
    window.show()

    app.exec()

if __name__ == "__main__":
    main()