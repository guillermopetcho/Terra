from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl  # Importamos QUrl

import sys
import urllib.parse

class GoogleMapsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Google Maps en Vivo")
        self.setGeometry(100, 100, 900, 700)  # Tamaño de la ventana

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout(self.central_widget)

        # Entrada de dirección
        self.entry_direccion = QLineEdit(self)
        self.entry_direccion.setPlaceholderText("Ingrese una dirección")
        layout.addWidget(self.entry_direccion)

        # Botón para buscar
        self.boton_buscar = QPushButton("Buscar en Google Maps", self)
        self.boton_buscar.clicked.connect(self.cargar_mapa)
        layout.addWidget(self.boton_buscar)

        # WebView para mostrar Google Maps en vivo
        self.webview = QWebEngineView(self)
        layout.addWidget(self.webview)

        # Cargar última búsqueda si existe
        self.cargar_ultima_busqueda()

    def cargar_mapa(self):
        """Carga Google Maps con la dirección ingresada."""
        direccion = self.entry_direccion.text()
        if not direccion:
            return

        # Generar URL de Google Maps
        url_maps = f"https://www.google.com/maps/search/{urllib.parse.quote(direccion)}"

        # Convertir a QUrl y cargar en WebView
        self.webview.setUrl(QUrl(url_maps))

        # Guardar la última búsqueda
        with open("ultima_busqueda.txt", "w") as f:
            f.write(direccion)
            
    def cargar_ultima_busqueda(self):
        """Carga la última dirección buscada al iniciar la app."""
        try:
            with open("ultima_busqueda.txt", "r") as f:
                ultima_direccion = f.read().strip()
                if ultima_direccion:
                    self.entry_direccion.setText(ultima_direccion)
                    self.cargar_mapa()
        except FileNotFoundError:
            pass  # Si no hay historial, no hace nada

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GoogleMapsApp()
    ventana.show()
    sys.exit(app.exec_())
