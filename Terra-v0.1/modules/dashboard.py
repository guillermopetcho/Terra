import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame
from .forms.control import ControlForm  # Correctamente importado
from .forms.chat_ia import ChatIAForm
from .forms.visualizacion_agricola import VisualizacionAgricolaForm
from .forms.analisis import AnalisisForm

class Dashboard(QMainWindow):
    def __init__(self, user_info=None):
        super().__init__()

        self.setWindowTitle("Panel de Control")
        self.setGeometry(100, 100, 900, 600)

        # Si no hay usuario autenticado, usar "Invitado"
        self.user_info = user_info if user_info else {"name": "Invitado"}

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal en cuadrícula
        layout = QGridLayout()

        # Cargar cada frame desde su formulario correspondiente
        self.section1 = self.create_frame(ControlForm(self.user_info))  # Aquí se importa desde control.py
        self.section2 = self.create_frame(ChatIAForm())
        self.section3 = self.create_frame(VisualizacionAgricolaForm())
        self.section4 = self.create_frame(AnalisisForm())

        # Ubicar los frames en la cuadrícula
        layout.addWidget(self.section1, 0, 0)
        layout.addWidget(self.section2, 0, 1)
        layout.addWidget(self.section3, 1, 0)
        layout.addWidget(self.section4, 1, 1)

        # Aplicar layout
        self.central_widget.setLayout(layout)

    def create_frame(self, widget):
        """Crea un frame y coloca el formulario dentro"""
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px solid #007ACC;
            border-radius: 10px;
            padding: 15px;
        """)
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(widget)
        frame.setLayout(frame_layout)
        return frame


# Para pruebas individuales
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard({"name": "Invitado"})  # Inicia con usuario "Invitado"
    dashboard.show()
    sys.exit(app.exec_())
