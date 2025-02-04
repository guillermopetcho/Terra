import sys
import json
import requests
import os
import ee
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from google_auth_oauthlib.flow import InstalledAppFlow

# ------------------- AUTENTICACIÓN GOOGLE OAUTH (USUARIO) -------------------

# Ruta al archivo JSON de credenciales de OAuth
OAUTH_CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "../client_secret.json")

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

    def authenticate(self):
        """Autenticación con Google usando OAuth"""
        SCOPES = ["https://www.googleapis.com/auth/userinfo.profile",
                  "https://www.googleapis.com/auth/userinfo.email", "openid"]

        if not os.path.exists(OAUTH_CREDENTIALS_FILE):
            self.label.setText("Error: No se encontró el archivo de credenciales OAuth")
            return

        try:
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

            # Obtener información del usuario autenticado
            user_info = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {creds.token}"}
            ).json()

            self.user_info = user_info
            self.label.setText(f"Bienvenido, {user_info['name']}!")

            # Redirigir al panel de control con el usuario autenticado
            self.open_dashboard(user_info)

        except Exception as e:
            self.label.setText(f"Error: {str(e)}")

    def open_dashboard(self, user_info):
        """Abrir el panel de control después de iniciar sesión"""
        from modules.dashboard import Dashboard
        self.hide()
        self.dashboard = Dashboard(user_info)
        self.dashboard.show()


# ------------------- AUTENTICACIÓN GOOGLE EARTH ENGINE -------------------

# Ruta al archivo JSON de credenciales de Earth Engine
EARTH_ENGINE_CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "../Earth Engine.json")

def autenticar_google_earth_engine():
    """Autentica Google Earth Engine usando el archivo JSON de servicio."""
    if not os.path.exists(EARTH_ENGINE_CREDENTIALS_FILE):
        print("❌ Error: No se encontró el archivo de credenciales de Earth Engine.")
        return

    try:
        ee.Initialize(ee.ServiceAccountCredentials(None, EARTH_ENGINE_CREDENTIALS_FILE))
        print("✅ Autenticación con Google Earth Engine exitosa")
    except Exception as e:
        print(f"❌ Error en la autenticación de Google Earth Engine: {e}")

# ------------------- INICIO DEL PROGRAMA -------------------
if __name__ == "__main__":
    # Primero autenticamos Google Earth Engine
    autenticar_google_earth_engine()
    
    # Luego iniciamos la aplicación con autenticación de usuario
    app = QApplication(sys.argv)
    window = GoogleLogin()
    window.show()
    sys.exit(app.exec_())
