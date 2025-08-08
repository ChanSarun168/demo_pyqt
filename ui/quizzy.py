from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QMessageBox, QButtonGroup
)
from PyQt6.QtCore import Qt


class QuizWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # Reference to MainWindow

        
        self.resize(500, 400)
        self.setStyleSheet("background-color: white;")

        # Connect to DB and get questions
        from db.database import Database  # import here to avoid circular issues
        self.db = Database()
        self.questions_data = self.db.get_all_questions()
        self.current_index = 0

        if not self.questions_data:
            QMessageBox.critical(self, "Error", "No questions found in the database.")
            self.close()
            return

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- Back button and header layout ---
        header_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(
            "QPushButton {"
            "background-color: #a3bffa;"
            "color: black;"
            "padding: 5px;"
            "border-radius: 8px;"
            "} QPushButton:hover {"
            "background-color: #dfefff;"
            "}"
        )
        back_btn.clicked.connect(self.goto_main)
        header_layout.addWidget(back_btn)

        title_label = QLabel("Quiz - PyQt6 + SQLite")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)
        # --------------------------------------

        self.question_label = QLabel()
        self.question_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        self.main_layout.addWidget(self.question_label)

        self.options_group = QButtonGroup()
        self.options_layout = QVBoxLayout()
        self.main_layout.addLayout(self.options_layout)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet(self.button_style("#a9dfbf"))
        self.submit_btn.clicked.connect(self.check_answer)
        self.main_layout.addWidget(self.submit_btn)

        self.load_question()

    def button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: black;
                font-weight: 600;
                padding: 10px 16px;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #dfefff;
                color: black;
            }}
        """

    def load_question(self):
        for btn in self.options_group.buttons():
            self.options_group.removeButton(btn)
            btn.deleteLater()

        q_data = self.questions_data[self.current_index]
        question_text, option_a, option_b, option_c, option_d, _ = q_data

        self.question_label.setText(f"Q{self.current_index + 1}: {question_text}")

        for option in [option_a, option_b, option_c, option_d]:
            radio_btn = QRadioButton(option)
            radio_btn.setStyleSheet("font-size: 14px; color: black;")
            self.options_group.addButton(radio_btn)
            self.options_layout.addWidget(radio_btn)

    def check_answer(self):
        selected_btn = self.options_group.checkedButton()
        if not selected_btn:
            QMessageBox.warning(self, "No Selection", "Please select an answer.")
            return

        selected_answer = selected_btn.text()
        correct_answer = self.questions_data[self.current_index][5]

        if selected_answer == correct_answer:
            QMessageBox.information(self, "Correct!", "That's the right answer!")
            self.current_index += 1
            if self.current_index < len(self.questions_data):
                self.load_question()
            else:
                QMessageBox.information(self, "Quiz Finished", "You have completed the quiz!")
                self.close()
        else:
            QMessageBox.critical(self, "Wrong!", f"The correct answer was: {correct_answer}\nPlease try again.")

    def goto_main(self):
        if self.main_window:
            self.main_window.show()
        self.close()
