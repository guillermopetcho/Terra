from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

# ✅ Importaciones relativas correctas
from .chat_ia import ChatIAForm
from .visualizacion_agricola import VisualizacionAgricolaForm
from .analisis import AnalisisForm

class ControlForm(QWidget):
    def __init__(self, user_info, parent=None):
        super().__init__(parent)

        self.user_info = user_info
        layout = QVBoxLayout()

        # Título de la sección
        label = QLabel("Panel de Control")
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)

        # Verificar si el usuario ha iniciado sesión
        if self.user_info.get("name") == "Invitado":
            self.label_status = QLabel("No has iniciado sesión")
            self.button_login = QPushButton("Ingresar Usuario")
            layout.addWidget(self.label_status)
            layout.addWidget(self.button_login)
        else:
            self.label_status = QLabel(f"Usuario: {self.user_info.get('name')}")
            layout.addWidget(self.label_status)

        self.setLayout(layout)
