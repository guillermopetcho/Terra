from PyQt5.QtWidgets import QApplication
from modules.dashboard import Dashboard

def main():
    app = QApplication([])
    dashboard = Dashboard({"name": "Invitado"})  # Usuario por defecto
    dashboard.show()
    app.exec_()

if __name__ == "__main__":
    main()
