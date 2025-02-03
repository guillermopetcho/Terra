import googlemaps
import folium
import os
import re
from config import GOOGLE_MAPS_API_KEY

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def dms_a_decimal(coord):
    """Convierte coordenadas DMS a decimal."""
    match = re.match(r"(\d+)°(\d+)'([\d\.]+)\"?([NSWE])", coord.strip())
    if match:
        grados, minutos, segundos, direccion = match.groups()
        decimal = float(grados) + float(minutos) / 60 + float(segundos) / 3600
        if direccion in ["S", "W"]:
            decimal *= -1
        return decimal
    return None

def procesar_coordenadas(direccion):
    """Detecta si la entrada es una dirección o coordenadas DMS y las convierte."""
    if "," in direccion:
        partes = direccion.split(",")
        if len(partes) == 2:
            lat = dms_a_decimal(partes[0].strip())
            lon = dms_a_decimal(partes[1].strip())
            if lat is not None and lon is not None:
                return lat, lon
    return None

def buscar_ubicacion(direccion):
    """Busca una dirección en Google Maps o convierte coordenadas DMS a decimal."""
    coordenadas = procesar_coordenadas(direccion)
    
    if coordenadas:
        return coordenadas  # Si se ingresaron coordenadas, se devuelven directamente.

    resultado = gmaps.geocode(direccion)
    
    if resultado:
        lat = resultado[0]["geometry"]["location"]["lat"]
        lon = resultado[0]["geometry"]["location"]["lng"]
        return lat, lon
    else:
        return None

def generar_mapa(direccion):
    """Genera un mapa en base a una dirección o coordenadas."""
    coordenadas = buscar_ubicacion(direccion)
    
    if coordenadas:
        lat, lon = coordenadas
        mapa = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], popup="Ubicación Seleccionada").add_to(mapa)

        # Asegurar que la carpeta "static" existe
        os.makedirs("static", exist_ok=True)

        # Guardar el mapa en la carpeta "static"
        ruta_mapa = "static/mapa.html"
        mapa.save(ruta_mapa)
        print(f"Mapa guardado en {ruta_mapa}")
        return ruta_mapa
    else:
        print("No se pudo generar el mapa.")
        return None
