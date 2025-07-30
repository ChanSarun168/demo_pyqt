import sys
from PyQt6.QtWidgets import QApplication
from ui.login_form import LoginForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginForm()
    login.show()
    sys.exit(app.exec())
