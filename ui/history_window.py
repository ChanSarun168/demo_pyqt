from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from db.database import Database

class HistoryWindow(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quiz History")
        self.resize(500, 400)
        self.username = username

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load_history()

    def load_history(self):
        db = Database()
        history = db.get_history(self.username)
        db.close()

        self.table.setRowCount(len(history))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Subject", "Score", "Total Questions", "Date"])

        for row_idx, row_data in enumerate(history):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
