from PyQt6.QtWidgets import (QApplication, QVBoxLayout,
                             QGridLayout, QWidget, QFrame)

from ManageDatabase import ManageBooksDatabase
from ModelWindow import ModelWindow

class AddStudentWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()
        student_file_label = self.add_label("Student File")
        first_name_label = self.add_label("First Name")
        last_name_label = self.add_label("Last Name")
        add_student_btn = self.add_button("Add Student", self.add_student)

        self.student_file_entry = self.add_line_edit()
        self.first_name_entry = self.add_line_edit()
        self.last_name_entry = self.add_line_edit()

        layout.addWidget(student_file_label, 0, 0)
        layout.addWidget(self.student_file_entry, 0, 1)
        layout.addWidget(first_name_label, 1, 0)
        layout.addWidget(self.first_name_entry, 1, 1)
        layout.addWidget(last_name_label, 2, 0)
        layout.addWidget(self.last_name_entry, 2, 1)
        layout.addWidget(add_student_btn, 3, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def add_student(self):
        file = self.student_file_entry.text()
        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()

        response = self.db_manager.insert(self.STUDENTS_TABLE, {"file": file, "first_name": first_name, "last_name": last_name})
        if response:
            response = self.db_manager.create_table(f"student{file}", [
                "i INT AUTO_INCREMENT",
                "bid INT",
                "issue_date DATE",
                "return_date DATE",
                "PRIMARY KEY(i)"
                ]
            )

            self.show_info("Student Added/Edited", "Student successfully added")
        elif response == False:
            # If response is False, is because book ID already exists
            self.db_manager.edit(self.STUDENTS_TABLE, id, "first_name", first_name)
            self.db_manager.edit(self.STUDENTS_TABLE, id, "last_name", last_name)

            if not response:
                self.show_info("Student Added/Edited", "Failed on edit student")
            else:
                self.show_info("Student Added/Edited", "Successfully edited student")

        else:
            self.show_info("Student Added/Edited", "Failed on add student")


class RemoveStudentWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QGridLayout()

        student_file_label = self.add_label("Student File")
        self.student_file_entry = self.add_line_edit()
        remove_student_btn = self.add_button("Remove Student", self.remove_student)

        layout.addWidget(student_file_label, 0, 0)
        layout.addWidget(self.student_file_entry, 0, 1)
        layout.addWidget(remove_student_btn, 1, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def remove_student(self):
        file = self.student_file_entry.text()
        response = self.db_manager.delete(self.STUDENTS_TABLE, "file", file)
        self.db_manager.delete_table(f"student{file}")
        if response:
            self.show_info("Student deleted", "Student successfully deleted")
        else:
            self.show_info("Student deleted", "Failed on delete student")


class ViewStudentsWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout()

        self.filter_entry = self.add_line_edit(self.filter_entry_changed)
        self.list_students_label = self.add_label("", {"font": "bold 11px Arial"})

        layout.addWidget(self.filter_entry)
        layout.addWidget(self.list_students_label)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.list_students()

    def list_students(self):
        students_string = "File\t\tFirst Name\t\tLast Name\n"
        students_string += self.db_manager.list(self.STUDENTS_TABLE)
        self.list_students_label.setText(students_string)

    def filter_entry_changed(self):
        entry_text = self.filter_entry.text()

        students_string = self.db_manager.list(self.STUDENTS_TABLE).split("\n")

        for index, line in enumerate(students_string):
            pos = line.find(entry_text)
            if pos == -1:
                students_string.pop(index)

        self.list_students_label.setText("\n".join(students_string))


class StudentsMainWindow(ModelWindow):
    def __init__(self, db_manager, title, styles=None):
        super().__init__(db_manager, title, styles)

        self.windows = list()
        self.title = title

        self.init_UI()

    def init_UI(self):
        title_label = self.add_label(self.title)
        add_student_btn = self.add_button("Add/Edit Student", self.add_student)
        remote_student_btn = self.add_button("Remove Student", self.remove_student)
        view_students_btn = self.add_button("View Students", self.view_students)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.VLine)
        frame.setFrameShadow(QFrame.Shadow.Sunken)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(frame)
        layout.addWidget(add_student_btn)
        layout.addWidget(remote_student_btn)
        layout.addWidget(view_students_btn)

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

    def add_student(self):
        self.add_book_window = AddStudentWindow(self.db_manager, "Add Book", self.styles)
        self.open_window_if_not_other_opened(self.add_book_window)

    def remove_student(self):
        self.remove_student_window = RemoveStudentWindow(self.db_manager, "Remove Student", self.styles)
        self.open_window_if_not_other_opened(self.remove_student_window)

    def view_students(self):
        self.view_students_window = ViewStudentsWindow(self.db_manager, "View Students", self.styles)
        self.open_window_if_not_other_opened(self.view_students_window)


def main():
    app = QApplication([])

    with open(".credentials-students", "r") as file:
        content = file.read()
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()

    window = StudentsMainWindow(manage_database, "Students Manager")
    window.show()

    app.exec()

if __name__ == "__main__":
    main()