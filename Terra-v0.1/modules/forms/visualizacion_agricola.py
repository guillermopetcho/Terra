import os
import ee
import json
import folium
import io
import base64
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

# ✅ Ruta correcta del archivo de credenciales
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Ir a la raíz del proyecto
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials", "Earth Engine.json")

# ✅ Verificar que el archivo de credenciales existe antes de inicializar
if not os.path.exists(CREDENTIALS_FILE):
    raise FileNotFoundError(f"❌ No se encontró el archivo de credenciales en: {CREDENTIALS_FILE}")

# ✅ Leer el archivo JSON manualmente para extraer la clave privada
with open(CREDENTIALS_FILE, "r") as file:
    credentials_data = json.load(file)

if "private_key" not in credentials_data or not credentials_data["private_key"]:
    raise ValueError("❌ El archivo de credenciales no tiene una clave privada válida.")

# ✅ Inicializar Google Earth Engine correctamente
credentials = ee.ServiceAccountCredentials(
    credentials_data["client_email"], CREDENTIALS_FILE
)
ee.Initialize(credentials)

print("✅ Google Earth Engine inicializado correctamente.")

class VisualizacionAgricolaForm(QWidget):
    def __init__(self):
        super().__init__()

        # Generar el mapa con folium
        self.map_html = self.generar_mapa()

        # Crear el visor web con QWebEngineView
        self.web_view = QWebEngineView()
        self.web_view.setHtml(self.map_html)  # Cargar el mapa en HTML

        # Botón para guardar coordenadas
        self.btn_guardar = QPushButton("Guardar Coordenadas")
        self.btn_guardar.clicked.connect(self.guardar_coordenadas)

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        layout.addWidget(self.btn_guardar)
        self.setLayout(layout)

    def generar_mapa(self):
        """Genera un mapa de Google Earth Engine con folium y lo devuelve como HTML"""
        m = folium.Map(location=[-30.67890, -60.12345], zoom_start=10)

        # Guardar el mapa en HTML
        map_html = io.BytesIO()
        m.save(map_html, close_file=False)
        return map_html.getvalue().decode()

    def guardar_coordenadas(self):
        """ Captura el centro del mapa y lo guarda localmente y en Google Drive """
        map_center = ee.Geometry.Point([-60.12345, -30.67890])  # Simulación de coordenadas
        coords = map_center.getInfo()["coordinates"]
        user_email = "usuario@gmail.com"  # Aquí deberías obtener el usuario autenticado

        from modules.utils import guardar_y_subir_coordenadas  # Importar la función desde utils
        guardar_y_subir_coordenadas(user_email, {"lat": coords[1], "lng": coords[0]})
