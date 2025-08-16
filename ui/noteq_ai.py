import os
from openai import OpenAI
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIWorker(QThread):
    """Background worker to fetch AI response without freezing UI."""
    finished = pyqtSignal(str)  # emits the AI's reply

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # change if you want another model
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant."},
                    {"role": "user", "content": self.prompt}
                ]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Error: {e}"
        self.finished.emit(reply)


class NodeQWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  

        self.setWindowTitle("Node Q - AI Study Assistant")
        self.resize(600, 700)
        self.setStyleSheet("background-color: white;")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header layout
        header_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(
            "QPushButton {background-color: #a3bffa; color: black; padding: 5px; border-radius: 8px;} "
            "QPushButton:hover {background-color: #dfefff;}"
        )
        back_btn.clicked.connect(self.goto_main)
        header_layout.addWidget(back_btn)

        header = QLabel("Node Q - Your AI Assistant")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        header_layout.addWidget(header)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Chat scroll area
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignmentFlag.AlignTop)

        chat_container = QWidget()
        chat_container.setLayout(self.chat_area)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(chat_container)
        main_layout.addWidget(scroll, stretch=1)

        # Text input area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Type your notes here...")
        self.text_input.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                color: black;
            }
        """)
        main_layout.addWidget(self.text_input)

        # Buttons layout
        button_layout = QHBoxLayout()
        upload_btn = QPushButton("Upload Image")
        upload_btn.setStyleSheet(
            "QPushButton {background-color: #a3bffa; color: black; padding: 10px 16px; border-radius: 8px;} "
            "QPushButton:hover {background-color: #dfefff;}"
        )
        upload_btn.clicked.connect(self.upload_image)
        button_layout.addWidget(upload_btn)

        send_btn = QPushButton("Send")
        send_btn.setStyleSheet(
            "QPushButton {background-color: #a9dfbf; color: black; padding: 10px 16px; border-radius: 8px;} "
            "QPushButton:hover {background-color: #dfefff;}"
        )
        send_btn.clicked.connect(self.send_text)
        button_layout.addWidget(send_btn)

        main_layout.addLayout(button_layout)

    def add_message_card(self, text, is_user=True, return_widget=False):
        """Add a chat bubble card to the chat area and optionally return the label widget."""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet(
            f"QFrame {{background-color: {'#a3bffa' if is_user else '#f2f2f2'}; "
            "border-radius: 10px; padding: 8px;}}"
        )

        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("color: black; font-size: 14px;")
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # allow copy

        layout = QVBoxLayout(card)
        layout.addWidget(label)

        wrapper = QHBoxLayout()
        if is_user:
            wrapper.addStretch()
            wrapper.addWidget(card)
        else:
            wrapper.addWidget(card)
            wrapper.addStretch()

        self.chat_area.addLayout(wrapper)

        if return_widget:
            return label  # so we can update it later

    def send_text(self):
        """Send user's text to OpenAI."""
        user_text = self.text_input.toPlainText().strip()
        if not user_text:
            return

        # Add user bubble
        self.add_message_card(user_text, is_user=True)
        self.text_input.clear()

        # Add AI placeholder bubble and keep reference to it
        self.ai_label = self.add_message_card("Thinking...", is_user=False, return_widget=True)

        # Call OpenAI in a separate thread
        self.worker = OpenAIWorker(user_text)
        self.worker.finished.connect(self.show_ai_reply)
        self.worker.start()

    def show_ai_reply(self, reply):
        """Update the AI's bubble dynamically."""
        if hasattr(self, 'ai_label') and self.ai_label:
            self.ai_label.setText(reply)
            self.ai_label.adjustSize()  # make the bubble resize to fit text


    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Upload Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.add_message_card(f"[Image uploaded: {file_path}]", is_user=True)

    def goto_main(self):
        if self.main_window:
            self.main_window.show()
        self.close()
