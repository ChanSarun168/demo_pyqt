from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from db.database import Database
from ui.main_window import MainWindow
from ui.register_form import RegisterForm

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.goto_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.input_username.text()
        password = self.input_password.text()
        user = self.db.validate_user(username, password)

        if user:
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def goto_register(self):
        self.main_window = RegisterForm()
        self.main_window.show()
        self.close()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()  # close login window
