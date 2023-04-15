from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget

class MainWindow(QMainWindow):
    def __init__(self, styles: dict=None):
        super().__init__()

        # Set window parameters
        self.setWindowTitle("Library Manager")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: black")

        self.DEFAULT_STYLES = {
            "background-color": "black",
            "color": "white",
            "font": "bold 20px Arial"
        }
        self.styles = self.set_styles(styles)

        self.init_UI()

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
        print(self.styles_string())
        label.setStyleSheet(self.styles_string())

        return label

    def init_UI(self):
        title_label = self.add_label("Library Manager")

        layout = QVBoxLayout()
        layout.addWidget(title_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()