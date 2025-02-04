from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
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
