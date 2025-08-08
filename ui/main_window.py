from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, 
    QGraphicsDropShadowEffect, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from ui.quizzy import QuizWindow
from ui.noteq_ai import NodeQWindow  # Import the NodeQWindow class

class CardWidget(QWidget):
    def __init__(self, icon_path, title, subtitle, description, button_color):
        super().__init__()
        self.setStyleSheet("""
            CardWidget {
                background-color: transparent;
            }
        """)

        card_container = QWidget()
        card_container.setStyleSheet("""
            background-color: #f5f5f5;
            border-radius: 15px;
            padding: 20px;
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor("#0000001A"))
        card_container.setGraphicsEffect(shadow)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        icon_container = QLabel()
        icon_container.setFixedSize(40, 40)
        icon_container.setStyleSheet(f"""
            background-color: {button_color};
            border-radius: 20px;
            padding: 5px;
        """)

        pixmap = QPixmap(icon_path).scaled(
            24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        icon_container.setPixmap(pixmap)
        icon_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_container)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        text_layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("font-size: 12px; color: #666;")
        text_layout.addWidget(subtitle_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 14px; color: #666;")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)

        layout.addLayout(text_layout)

        arrow_button = QPushButton()
        arrow_button.setFixedSize(30, 30)
        arrow_button.setStyleSheet(f"""
            background-color: {button_color};
            border: none;
            border-radius: 15px;
        """)
        layout.addWidget(arrow_button)

        card_container_layout = QHBoxLayout(card_container)
        card_container_layout.addLayout(layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(card_container)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            MainWindow {
                background-color: white;
            }
        """)
        self.setWindowTitle("Node Q")
        self.resize(556, 691)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 50, 20, 20)

        title_label = QLabel("Ready to Learn? Choose Your Path!")
        title_label.setStyleSheet("font-size: 30px; font-weight: 700; color: black;")
        main_layout.addWidget(title_label)

        node_q_card = CardWidget(
            "image/mingcute_ai-fill.png",
            "Node Q",
            "Your AI Assistant",
            "Use AI to study smarter. Generate questions from your lesson notes and keep important points organized for quick review.",
            "#a3bffa"  # Light purple
        )
        node_q_card.mousePressEvent = lambda event: self.open_node_q_window()
        main_layout.addWidget(node_q_card)

        quizzy_card = CardWidget(
            "image/material-symbols_quiz-rounded.png",
            "Quizzy",
            "Project Manager",
            "Practice what you've learned. Get auto-generated exercises to help you prepare for exams and track your progress.",
            "#a9dfbf"  # Light green
        )
        quizzy_card.mousePressEvent = lambda event: self.open_quiz()
        main_layout.addWidget(quizzy_card)

        self.setCentralWidget(central_widget)

    def open_node_q_window(self):
        self.node_q_window = NodeQWindow(main_window=self)
        self.node_q_window.show()
        self.close()
    def open_quiz(self):
        self.quiz_window = QuizWindow(main_window=self)
        self.quiz_window.show()
        self.hide()
