from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
)

class NodeQWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # store reference to main window

        self.setWindowTitle("Node Q - AI Study Assistant")
        self.resize(600, 700)
        self.setStyleSheet("background-color: white;")

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header layout (Back button + Title)
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

        header = QLabel("Node Q - Your AI Assistant")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        header_layout.addWidget(header)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

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
        main_layout.addWidget(self.text_input, stretch=1)

        # Upload & Send buttons
        button_layout = QHBoxLayout()
        upload_btn = QPushButton("Upload Image")
        upload_btn.setStyleSheet(
            "QPushButton {"
            "background-color: #a3bffa;"
            "color: black;"
            "padding: 10px 16px;"
            "border: none;"
            "border-radius: 8px;"
            "} QPushButton:hover {"
            "background-color: #dfefff;"
            "}"
        )
        upload_btn.clicked.connect(self.upload_image)
        button_layout.addWidget(upload_btn)

        send_btn = QPushButton("Send")
        send_btn.setStyleSheet(
            "QPushButton {"
            "background-color: #a9dfbf;"
            "color: black;"
            "padding: 10px 16px;"
            "border: none;"
            "border-radius: 8px;"
            "} QPushButton:hover {"
            "background-color: #dfefff;"
            "}"
        )
        send_btn.clicked.connect(self.send_text)
        button_layout.addWidget(send_btn)

        main_layout.addLayout(button_layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Upload Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            print(f"📎 Uploaded Image: {file_path}")

    def send_text(self):
        user_text = self.text_input.toPlainText().strip()
        if user_text:
            print(f"💬 User Message: {user_text}")
            self.text_input.clear()

    def goto_main(self):
        if self.main_window:
            self.main_window.show()
        self.close()
