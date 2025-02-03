from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AnalisisForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Análisis de datos en desarrollo..."))
        self.setLayout(layout)
