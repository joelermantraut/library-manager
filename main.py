from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QGridLayout, QLabel, QWidget, QPushButton,
                             QLineEdit)

class ModelWindow(QMainWindow):
    def __init__(self, title, styles: dict=None):
        super().__init__()

        self.x = 100
        self.y = 100
        self.width = 500
        self.height = 300

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
    
    def add_line_edit(self):
        line_edit = QLineEdit(self)

        return line_edit


class AddBookWindow(ModelWindow):
    def __init__(self, title, styles=None):
        super().__init__(title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()
        book_ID_label = self.add_label("Book ID")
        book_title_label = self.add_label("Title")
        book_author_label = self.add_label("Author")
        book_status_label = self.add_label("Status")

        book_ID_entry = self.add_line_edit()
        book_title_entry = self.add_line_edit()
        book_author_entry = self.add_line_edit()
        book_status_entry = self.add_line_edit()

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(book_ID_entry, 0, 1)
        layout.addWidget(book_title_label, 1, 0)
        layout.addWidget(book_title_entry, 1, 1)
        layout.addWidget(book_author_label, 2, 0)
        layout.addWidget(book_author_entry, 2, 1)
        layout.addWidget(book_status_label, 3, 0)
        layout.addWidget(book_status_entry, 3, 1)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


class ViewBooksWindow(ModelWindow):
    def __init__(self, title, styles=None):
        super().__init__(title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout()

        filter_entry = self.add_line_edit()
        list_books_label = self.add_label("books -----------------------------")

        layout.addWidget(filter_entry)
        layout.addWidget(list_books_label)
        
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


class IssueBookWindow(ModelWindow):
    def __init__(self, title, styles=None):
        super().__init__(title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()

        book_ID_label = self.add_label("Book ID")
        book_ID_entry = self.add_line_edit()
        issue_book_btn = self.add_button("Issue Book")

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(book_ID_entry, 0, 1)
        layout.addWidget(issue_book_btn, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


class ReturnBookWindow(ModelWindow):
    def __init__(self, title, styles=None):
        super().__init__(title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()

        book_ID_label = self.add_label("Book ID")
        book_ID_entry = self.add_line_edit()
        return_book_btn = self.add_button("Return Book")

        layout.addWidget(book_ID_label, 0, 0)
        layout.addWidget(book_ID_entry, 0, 1)
        layout.addWidget(return_book_btn, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


class MainWindow(ModelWindow):
    def __init__(self, title, styles=None):
        super().__init__(title, styles)

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
        self.add_book_window = AddBookWindow("Add Book", self.styles)
        self.add_book_window.show()

    def view_books(self):
        self.view_books_window = ViewBooksWindow("View Books", self.styles)
        self.view_books_window.show()

    def issue_book(self):
        self.issue_book_window = IssueBookWindow("Issue Book", self.styles)
        self.issue_book_window.show()

    def return_book(self):
        self.return_book_window = ReturnBookWindow("Return Book", self.styles)
        self.return_book_window.show()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow("Library Manager")
    window.show()

    app.exec()