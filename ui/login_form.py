# Import necessary PyQt6 modules for UI components and functionality
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox
from db.database import Database  # Your custom database class for user validation
from ui.main_window import MainWindow  # The main application window after login
from ui.register_form import RegisterForm  # The registration form window
from PyQt6.QtCore import Qt  # Qt constants (not directly used here but imported)

# Define the LoginForm class which is a QWidget (a basic window/container)
class LoginForm(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of QWidget

        # Set the style for this widget (background color)
        self.setStyleSheet("""
            LoginForm {
                background-color: white;
            }
        """)

        self.setWindowTitle("Login")  # Set the window title
        self.resize(556, 691)  # Set the size of the login window

        self.db = Database()  # Create an instance of your custom Database class
        self.setup_ui()  # Call method to setup the UI elements

    def setup_ui(self):
        # Use a vertical layout to arrange widgets from top to bottom
        layout = QVBoxLayout()  
        layout.setContentsMargins(30, 30, 30, 30)  # Add padding around the edges
        layout.setSpacing(15)  # Space between widgets

        # Greeting label
        self.title_label = QLabel()
        self.title_label.setText("""
            <span style='font-size: 30px; font-weight: 700; color: black;'>Hi, Welcome! 👋</span>
        """)
        layout.addWidget(self.title_label)  # Add to layout

        # Username label and input field
        self.label_username = QLabel("<span style='font-size:16px; color:#000;'>Username:</span>")
        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("padding:20px; background-color:white; border: 1px solid #B0B0B0; color:black; border-radius:12px")
        self.input_username.setPlaceholderText("Enter username")  # Hint text
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        # Password label and input field
        self.label_password = QLabel("<span style='font-size:16px; color:#000;'>Password:</span>")
        self.input_password = QLineEdit()
        self.input_password.setStyleSheet("padding:20px; background-color:white; border: 1px solid #B0B0B0; color:black; border-radius:12px; margin-bottom:20px;")
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password characters
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        # Login button
        self.login_button = QPushButton("Log in")
        self.login_button.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
        self.login_button.clicked.connect(self.check_login)  # Call check_login when clicked
        layout.addWidget(self.login_button)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
        self.register_button.clicked.connect(self.goto_register)  # Go to register form when clicked
        layout.addWidget(self.register_button)

        self.setLayout(layout)  # Set the layout for the widget

    def check_login(self):
        # Get the entered username and password
        username = self.input_username.text()
        password = self.input_password.text()

        # Validate the credentials using your Database class
        user = self.db.validate_user(username, password)

        if user:
            # If valid, show success message and open the main app window
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_main_window()
        else:
            # If invalid, show error message
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def goto_register(self):
        # Open the RegisterForm window and close the login form
        self.main_window = RegisterForm()
        self.main_window.show()
        self.close()

    def open_main_window(self):
        # Open the MainWindow (main application screen) and close the login form
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
