import tkinter as tk
from tkinter import messagebox
import webbrowser
import urllib.parse

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Google Maps - Búsqueda en Vivo")
        self.geometry("500x200")

        # Frame para la entrada de dirección y botón
        frame_top = tk.Frame(self)
        frame_top.pack(pady=10)

        self.label = tk.Label(frame_top, text="Buscar en Google Maps:", font=("Arial", 12))
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry_direccion = tk.Entry(frame_top, width=50)
        self.entry_direccion.pack(side=tk.LEFT, padx=5)

        self.boton_buscar = tk.Button(frame_top, text="Buscar", command=self.abrir_google_maps)
        self.boton_buscar.pack(side=tk.LEFT, padx=5)

        # Cargar la última búsqueda si existe
        self.cargar_ultima_busqueda()

    def abrir_google_maps(self):
        """Abre Google Maps en el navegador predeterminado con la dirección ingresada."""
        direccion = self.entry_direccion.get()
        if not direccion:
            messagebox.showerror("Error", "Por favor, ingrese una ubicación.")
            return

        # Crear la URL de Google Maps
        url_maps = f"https://www.google.com/maps/search/{urllib.parse.quote(direccion)}"

        # Abrir en el navegador predeterminado
        webbrowser.open(url_maps)

        # Guardar la última búsqueda
        with open("ultima_busqueda.txt", "w") as f:
            f.write(direccion)

    def cargar_ultima_busqueda(self):
        """Carga la última dirección buscada al iniciar la app."""
        try:
            with open("ultima_busqueda.txt", "r") as f:
                ultima_direccion = f.read().strip()
                if ultima_direccion:
                    self.entry_direccion.insert(0, ultima_direccion)
        except FileNotFoundError:
            pass  # Si no hay historial, no hace nada
