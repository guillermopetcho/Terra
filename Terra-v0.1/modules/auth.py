import sys
import json
import requests
import os
import ee
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from database import usuario_existe, guardar_usuario
from google.auth.transport.requests import Request


# Ruta a los archivos JSON
OAUTH_CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "../client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "../user_token.json")  # Guardaremos el token aquí

class GoogleLogin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Iniciar Sesión con Google")
        self.setGeometry(100, 100, 400, 200)

        # Etiqueta de estado
        self.label = QLabel("Por favor, inicia sesión con Google", self)
        self.label.setGeometry(50, 50, 300, 20)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar Sesión", self)
        self.login_button.setGeometry(130, 100, 150, 40)
        self.login_button.clicked.connect(self.authenticate)

        self.user_info = None

        # Intentar cargar credenciales guardadas
        self.load_saved_credentials()


    def authenticate(self):
        """Autenticación con Google usando OAuth"""
        SCOPES = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
            "https://www.googleapis.com/auth/drive.file"  # 🚀 Permiso para escribir en Google Drive
        ]

        if not os.path.exists(OAUTH_CREDENTIALS_FILE):
            self.label.setText("Error: No se encontró el archivo de credenciales OAuth")
            return

        try:
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

            # Guardar credenciales en JSON
            with open(TOKEN_FILE, "w") as token_file:
                token_file.write(creds.to_json())  # Guarda todo, incluido el refresh_token

            # Obtener información del usuario autenticado
            user_info = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {creds.token}"}
            ).json()

            self.user_info = user_info

            # Verificar si el usuario ya existe en la base de datos
            if not usuario_existe(user_info["email"]):
                print("Nuevo usuario detectado. Creando cuenta...")
                guardar_usuario(user_info["id"], user_info["name"], user_info["email"], user_info["picture"])
            else:
                print(f"Bienvenido de nuevo, {user_info['name']}!")

            self.label.setText(f"Bienvenido, {user_info['name']}!")
            self.open_dashboard(user_info)

        except Exception as e:
            self.label.setText(f"Error: {str(e)}")


def load_saved_credentials(self):
    """Carga credenciales guardadas y solo inicia sesión si el token sigue siendo válido."""
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as token_file:
                creds_data = json.load(token_file)

            creds = Credentials.from_authorized_user_info(creds_data)

            # Verificamos si el token sigue siendo válido
            if creds and creds.valid:
                print("✅ Sesión encontrada. Iniciando sin autenticación.")
                self.label.setText("Sesión encontrada. Ingresando...")

                self.user_info = requests.get(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    headers={"Authorization": f"Bearer {creds.token}"}
                ).json()

                self.open_dashboard(self.user_info)
            else:
                print("🔴 Token expirado, se requiere autenticación nueva.")
                self.label.setText("Tu sesión ha caducado. Inicia sesión nuevamente.")

        except Exception as e:
            print(f"⚠️ Error al cargar credenciales guardadas: {e}")

    def open_dashboard(self, user_info):
        """Abrir el panel de control después de iniciar sesión"""
        from modules.dashboard import Dashboard
        self.hide()
        self.dashboard = Dashboard(user_info)
        self.dashboard.show()

