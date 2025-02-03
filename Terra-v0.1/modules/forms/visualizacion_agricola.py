from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class VisualizacionAgricolaForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Visualización Agrícola en desarrollo..."))
        self.setLayout(layout)
