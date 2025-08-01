import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
from ui.login_form import LoginForm
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load custom font
    font_id = QFontDatabase.addApplicationFont("assets/fonts/Poppins-Regular.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 12))
    else:
        print("⚠️ Failed to load custom font.")

    login = LoginForm()
    login.show()
    sys.exit(app.exec())
