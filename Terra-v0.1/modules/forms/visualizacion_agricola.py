import ee
import folium
import geemap
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtCore import QUrl


class VisualizacionAgricolaForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Inicializar Google Earth Engine con las credenciales
        CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "../../Earth Engine.json")
        ee.Initialize(ee.ServiceAccountCredentials(None, CREDENTIALS_FILE))

        # Crear un mapa con folium y geemap
        map_center = [-27.0, -60.0]  # Ubicación inicial (ejemplo: Chaco, Argentina)
        m = geemap.Map(center=map_center, zoom=6)

        # Cargar imagen satelital Sentinel-2
        dataset = ee.ImageCollection('COPERNICUS/S2').filterDate('2023-01-01', '2023-12-31').median()
        vis_params = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}
        m.addLayer(dataset, vis_params, "Sentinel-2")

        # Guardar el mapa en un archivo HTML
        map_file = "map.html"
        m.to_html(map_file)

        # Mostrar el mapa en la aplicación usando QWebEngineView
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(map_file)))
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)
