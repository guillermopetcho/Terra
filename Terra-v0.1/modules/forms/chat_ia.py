from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ChatIAForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chat IA en desarrollo..."))
        self.setLayout(layout)