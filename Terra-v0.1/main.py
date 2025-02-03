import sys
from PyQt5.QtWidgets import QApplication
from modules.qt_ui import GoogleMapsApp  # Importamos la clase de la interfaz

def main():
    """Ejecuta la aplicación de Google Maps en vivo."""
    app = QApplication(sys.argv)
    ventana = GoogleMapsApp()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
