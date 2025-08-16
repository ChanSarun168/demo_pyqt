import os
import json
import re
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QRadioButton, QMessageBox, QButtonGroup, QComboBox
)
from PyQt6.QtCore import Qt
from openai import OpenAI
from dotenv import load_dotenv
from db.database import Database  # Your database file

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QuizWindow(QMainWindow):
    def __init__(self, main_window=None, username=None):
        super().__init__()
        self.main_window = main_window
        self.username = username  # Save username for history
        self.setWindowTitle("AI Quiz App")
        self.resize(500, 500)
        self.setStyleSheet("background-color: #FF98D9;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # --- Subject selection ---
        self.layout.addWidget(QLabel("Select Subject:"))
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["Math", "Physics", "Chemistry"])
        self.layout.addWidget(self.subject_combo)

        # --- Subject selection ---
        self.layout.addWidget(QLabel("Select Level:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Beginner", "Middle", "Advance"])
        self.layout.addWidget(self.level_combo)

        self.generate_btn = QPushButton("Generate Quiz (AI)")
        self.generate_btn.clicked.connect(self.generate_quiz_ai)
        self.layout.addWidget(self.generate_btn)

        # Placeholders
        self.questions_data = []
        self.current_index = 0
        self.options_group = None
        self.options_layout = None
        self.question_label = None
        self.submit_btn = None
        self.score = 0

    # --- Generate Quiz with AI ---
    def generate_quiz_ai(self):
        subject = self.subject_combo.currentText()
        level = self.level_combo.currentText()
        self.questions_data = self.call_openai_generate(subject,level)
        if not self.questions_data:
            QMessageBox.critical(self, "Error", "AI did not return questions.")
            return

        self.current_index = 0
        self.score = 0
        self.subject_combo.hide()
        self.generate_btn.hide()

        # --- Load first question UI ---
        self.question_label = QLabel()
        self.question_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        self.layout.addWidget(self.question_label)

        self.options_group = QButtonGroup()
        self.options_layout = QVBoxLayout()
        self.layout.addLayout(self.options_layout)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.check_answer)
        self.submit_btn.setStyleSheet(self.button_style("#a9dfbf"))
        self.layout.addWidget(self.submit_btn)

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

    # --- Load question ---
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

    # --- Check answer ---
    def check_answer(self):
        selected_btn = self.options_group.checkedButton()
        if not selected_btn:
            QMessageBox.warning(self, "No Selection", "Please select an answer.")
            return

        selected_answer = selected_btn.text()
        correct_answer = self.questions_data[self.current_index][5]

        if selected_answer == correct_answer:
            self.score += 1
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Wrong!")
            msg.setText(f"The correct answer was: {correct_answer}")
            explain_btn = msg.addButton("Explain", QMessageBox.ButtonRole.ActionRole)
            msg.addButton(QMessageBox.StandardButton.Ok)
            msg.exec()

            if msg.clickedButton() == explain_btn:
                explanation = self.call_openai_explain(
                    self.questions_data[self.current_index][0],
                    correct_answer
                )
                QMessageBox.information(self, "Explanation", explanation)

        self.current_index += 1
        if self.current_index < len(self.questions_data):
            self.load_question()
        else:
            self.show_result()

    # --- Show final result ---
    def show_result(self):
        total_questions = len(self.questions_data)

        # Clear previous widgets
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Show score
        score_label = QLabel(f"You completed the quiz!\n\nScore: {self.score}/{total_questions}")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.layout.addWidget(score_label)

        # Button to return to main window
        back_btn = QPushButton("Back to Main Menu")
        back_btn.setStyleSheet(self.button_style("#a9dfbf"))
        back_btn.clicked.connect(self.return_to_main)
        self.layout.addWidget(back_btn)

        # Save history
        if self.username:
            db = Database()
            db.save_history(
                username=self.username,
                subject=self.subject_combo.currentText(),
                score=self.score,
                total_questions=total_questions
            )
            db.close()

    def return_to_main(self):
        """Return to the main window"""
        if self.main_window:
            self.main_window.show()
        self.close()

    # --- Call OpenAI to generate questions ---
    def call_openai_generate(self, subject , level ):
        prompt = f"""
            Generate 5 multiple choice questions (with 4 options and correct answer) about {subject} in {level} level.
            Return ONLY valid JSON in this exact format, nothing else:

            [
            {{
                "question": "Your question?",
                "options": ["A", "B", "C", "D"],
                "answer": "Correct option"
            }},
            ...
            ]
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content

            # --- Extract JSON robustly ---
            match = re.search(r'(\[.*\])', text, re.DOTALL)
            if match:
                questions_json = json.loads(match.group(1))
                return [
                    (
                        q["question"],
                        q["options"][0],
                        q["options"][1],
                        q["options"][2],
                        q["options"][3],
                        q["answer"]
                    )
                    for q in questions_json
                ]
            else:
                raise ValueError("No JSON found in AI response")
        except Exception as e:
            print("Error generating questions:", e)
            return []

    # --- Call OpenAI to explain wrong answers ---
    def call_openai_explain(self, question, answer):
        prompt = f"Explain why the correct answer to this question is '{answer}': {question}"
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print("Error explaining question:", e)
            return "Failed to get explanation from AI."
    def save_history(self, username, subject, score, total_questions):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO history (username, subject, score, total_questions)
            VALUES (?, ?, ?, ?)
        ''', (username, subject, score, total_questions))
        self.conn.commit()

