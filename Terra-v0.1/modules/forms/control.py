from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from modules.utils import subir_a_drive, descargar_desde_drive  # Importar funciones de subida y descarga
import os

class ControlForm(QWidget):
    def __init__(self, user_info, parent=None):
        super().__init__(parent)

        self.user_info = user_info
        layout = QVBoxLayout()

        # Título de la sección
        label = QLabel("Panel de Control")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)

        # Si el usuario no ha iniciado sesión, mostrar botón para iniciar sesión
        if self.user_info.get("name") == "Invitado":
            self.label_status = QLabel("No has iniciado sesión")
            self.label_status.setAlignment(Qt.AlignCenter)

            self.button_login = QPushButton("Ingresar con Google")
            self.button_login.setStyleSheet("""
                background-color: #007ACC;
                color: white;
                border-radius: 5px;
                padding: 8px;
            """)
            self.button_login.clicked.connect(self.abrir_login)

            layout.addWidget(self.label_status)
            layout.addWidget(self.button_login)
        else:
            # Mostrar el usuario autenticado
            self.label_status = QLabel(f"Usuario: {self.user_info.get('name')}")
            self.label_status.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.label_status)

            # Botón de Cerrar Sesión
            self.button_logout = QPushButton("Cerrar Sesión")
            self.button_logout.setStyleSheet("""
                background-color: #CC0000;
                color: white;
                border-radius: 5px;
                padding: 8px;
            """)
            self.button_logout.clicked.connect(self.cerrar_sesion)
            layout.addWidget(self.button_logout)

            # ---------------- NUEVOS BOTONES ----------------
            self.btn_subir_drive = QPushButton("📤 Subir Coordenadas a Google Drive")
            self.btn_subir_drive.setStyleSheet("""
                background-color: #28a745;
                color: white;
                border-radius: 5px;
                padding: 8px;
            """)
            self.btn_subir_drive.clicked.connect(self.subir_a_drive)
            layout.addWidget(self.btn_subir_drive)

            self.btn_descargar_drive = QPushButton("📥 Descargar Coordenadas desde Google Drive")
            self.btn_descargar_drive.setStyleSheet("""
                background-color: #17a2b8;
                color: white;
                border-radius: 5px;
                padding: 8px;
            """)
            self.btn_descargar_drive.clicked.connect(self.descargar_desde_drive)
            layout.addWidget(self.btn_descargar_drive)
            # ------------------------------------------------

        self.setLayout(layout)

    def abrir_login(self):
        """Abrir la ventana de autenticación con Google"""
        from modules.auth import GoogleLogin
        self.hide()
        self.login_window = GoogleLogin()
        self.login_window.show()

    def cerrar_sesion(self):
        """Cerrar sesión y volver al estado de 'Invitado'"""
        self.user_info["name"] = "Invitado"
        self.label_status.setText("No has iniciado sesión")

        # Ocultar los botones de Google Drive
        self.btn_subir_drive.hide()
        self.btn_descargar_drive.hide()

        # Ocultar el botón de cerrar sesión y mostrar el de inicio de sesión
        self.button_logout.hide()
        self.button_login = QPushButton("Ingresar con Google")
        self.button_login.setStyleSheet("""
            background-color: #007ACC;
            color: white;
            border-radius: 5px;
            padding: 8px;
        """)
        self.button_login.clicked.connect(self.abrir_login)

        self.layout().addWidget(self.button_login)

    def subir_a_drive(self):
        """ Ejecuta la subida de coordenadas a Google Drive """
        subir_a_drive()

    def descargar_desde_drive(self):
        """ Ejecuta la descarga de coordenadas desde Google Drive """
        descargar_desde_drive()


    def subir_a_drive(self):
        """ Ejecuta la subida de coordenadas a Google Drive """
        subir_a_drive()

    def descargar_desde_drive(self):
        """ Ejecuta la descarga de coordenadas desde Google Drive """
        descargar_desde_drive()