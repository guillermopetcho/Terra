import sys
from PyQt5.QtWidgets import QApplication
from modules.dashboard import Dashboard  # Asegúrate de que está bien escrito

def main():
    """Ejecuta la aplicación mostrando el Panel de Control."""
    app = QApplication(sys.argv)
    dashboard = Dashboard({"name": "Invitado"})  # Usuario por defecto
    dashboard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
