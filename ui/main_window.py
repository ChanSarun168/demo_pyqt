from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect , QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap , QColor

class CardWidget(QWidget):
    def __init__(self, icon_path, title, subtitle, description, button_color):
        super().__init__()
        self.setStyleSheet("""
            CardWidget {
                background-color: transparent;
            }
        """)

        # Outer widget for shadow
        card_container = QWidget()
        card_container.setStyleSheet("""
            background-color: #f5f5f5;
            border-radius: 15px;
            padding: 20px;
        """)

        # Add shadow effect to the container
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor("#0000001A"))
        card_container.setGraphicsEffect(shadow)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)

        # Text layout
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

        # Arrow button
        arrow_button = QPushButton()
        arrow_button.setStyleSheet("""
            background-color: %s;
            border: none;
            border-radius: 15px;
            width: 30px;
            height: 30px;
        """ % button_color)
        layout.addWidget(arrow_button)

        # Set layout for the container
        card_container_layout = QHBoxLayout(card_container)
        card_container_layout.addLayout(layout)

        # Main layout to hold the container
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

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 50, 20, 20)

        # Title label
        title_label = QLabel("Ready to Learn? Choose Your Path!")
        title_label.setStyleSheet("font-size: 30px; font-weight: 700; color: black;")
        main_layout.addWidget(title_label)

        # Card 1: Node Q
        node_q_card = CardWidget(
            "path/to/star_icon.png",  # Replace with actual icon path
            "Node Q",
            "Your AI Assistant",
            "Use AI to study smarter. Generate questions from your lesson notes and keep important points organized for quick review.",
            "#a3bffa"  # Light purple for arrow
        )
        main_layout.addWidget(node_q_card)

        # Card 2: Quizzy
        quizzy_card = CardWidget(
            "path/to/question_icon.png",  # Replace with actual icon path
            "Quizzy",
            "Project Manager",
            "Practice what you've learned. Get auto-generated exercises to help you prepare for exams and track your progress.",
            "#a9dfbf"  # Light green for arrow
        )
        main_layout.addWidget(quizzy_card)

        self.setCentralWidget(central_widget)