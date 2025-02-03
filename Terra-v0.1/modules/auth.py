import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from google_auth_oauthlib.flow import InstalledAppFlow

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
        """Autenticación con Google OAuth 2.0"""
        SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]

        try:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

            # Obtener información del usuario
            user_info = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {creds.token}"}
            ).json()

            self.user_info = user_info
            self.label.setText(f"Bienvenido, {user_info['name']}!")

            # Abrir el panel de control con la sesión iniciada
            self.open_dashboard(user_info)

        except Exception as e:
            self.label.setText(f"Error: {str(e)}")

    def open_dashboard(self, user_info):
        """Abrir el panel de control después de iniciar sesión"""
        from modules.dashboard import Dashboard
        self.hide()
        self.dashboard = Dashboard(user_info)
        self.dashboard.show()

# Para pruebas individuales
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoogleLogin()
    window.show()
    sys.exit(app.exec_())
