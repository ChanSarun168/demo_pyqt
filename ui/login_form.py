from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox
from db.database import Database
from ui.main_window import MainWindow
from ui.register_form import RegisterForm
from PyQt6.QtCore import Qt

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            LoginForm {
                background-color: white;
            }
        """)
        self.setWindowTitle("Login")
        self.resize(556, 691)
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()  
        layout.setContentsMargins(30, 30, 30, 30) 
        layout.setSpacing(15)

        self.title_label = QLabel()
        self.title_label.setText("""
            <span style='font-size: 30px; font-weight: 700; color: black;'>Hi, Welcome! 👋</span>
        """)
        layout.addWidget(self.title_label)

        self.label_username = QLabel("<span style='font-size:16px; color:#000;'>Username:</span>")
        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("padding:20px; background-color:white; border: 1px solid #B0B0B0; color:black; border-radius:12px")
        self.input_username.setPlaceholderText("Enter username")
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("<span style='font-size:16px; color:#000;'>Password:</span>")
        self.input_password = QLineEdit()
        self.input_password.setStyleSheet("padding:20px; background-color:white; border: 1px solid #B0B0B0; color:black; border-radius:12px; margin-bottom:20px;")
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.login_button = QPushButton("Log in")
        self.login_button.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
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
        self.close()