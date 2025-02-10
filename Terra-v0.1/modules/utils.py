import os
import csv
import sqlite3
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# ✅ Rutas de credenciales y almacenamiento local
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Ir a la raíz del proyecto
CSV_FILE = os.path.join(BASE_DIR, "data", "coordenadas.csv")
DB_FILE = os.path.join(BASE_DIR, "database", "coordenadas.db")
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials", "drive_credentials.json")

def sincronizar_sqlite_con_csv():
    """ Sincroniza los datos de la base de datos SQLite con el archivo CSV """
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)  # Asegura que la carpeta de datos exista

    # Conectar a la base de datos
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT user_email, lat, lng FROM coordenadas")
    data = cursor.fetchall()
    conn.close()

    # Guardar en CSV
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Usuario", "Latitud", "Longitud"])  # Encabezados
        writer.writerows(data)  # Escribir filas desde SQLite

    print(f"✅ Base de datos sincronizada con {CSV_FILE}")

def guardar_en_sqlite(user_email, coords):
    """ Guarda coordenadas en una base de datos SQLite y sincroniza con CSV """
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)  # Asegura que la carpeta database exista
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coordenadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            lat REAL,
            lng REAL
        )
    """)

    cursor.execute("INSERT INTO coordenadas (user_email, lat, lng) VALUES (?, ?, ?)", 
                   (user_email, coords["lat"], coords["lng"]))

    conn.commit()
    conn.close()

    # Sincronizar con CSV
    sincronizar_sqlite_con_csv()

    print(f"✅ Coordenadas guardadas en SQLite ({DB_FILE}) y sincronizadas con CSV")

def subir_a_drive():
    """ Sube el archivo CSV a Google Drive """
    if not os.path.exists(CSV_FILE):
        print("⚠️ No hay coordenadas guardadas localmente. No se puede subir el archivo.")
        return

    try:
        # Configurar autenticación con Google Drive
        gauth = GoogleAuth()

        # Verificar si ya hay credenciales guardadas
        if os.path.exists(CREDENTIALS_FILE):
            gauth.LoadCredentialsFile(CREDENTIALS_FILE)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        # Guardar credenciales para futuros usos
        gauth.SaveCredentialsFile(CREDENTIALS_FILE)

        # Conectar con Google Drive
        drive = GoogleDrive(gauth)

        # Subir el archivo CSV en lugar de la base de datos SQLite
        file_drive = drive.CreateFile({"title": "coordenadas.csv"})
        file_drive.SetContentFile(CSV_FILE)
        file_drive.Upload()

        print("✅ Coordenadas subidas correctamente a Google Drive.")

    except Exception as e:
        print(f"❌ Error al subir a Google Drive: {e}")

def descargar_desde_drive():
    """ Descarga el archivo CSV desde Google Drive y lo convierte en SQLite """
    try:
        # Configurar autenticación con Google Drive
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(CREDENTIALS_FILE)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        # Conectar con Google Drive
        drive = GoogleDrive(gauth)

        # Buscar archivo `coordenadas.csv` en Drive
        file_list = drive.ListFile({'q': "title='coordenadas.csv'"}).GetList()
        if not file_list:
            print("⚠️ No se encontró `coordenadas.csv` en Google Drive.")
            return

        # Descargar el archivo más reciente
        file_drive = file_list[0]
        file_drive.GetContentFile(CSV_FILE)
        print(f"✅ Archivo `{CSV_FILE}` descargado desde Google Drive.")

        # Convertir el CSV a SQLite
        csv_a_sqlite()

    except Exception as e:
        print(f"❌ Error al descargar desde Google Drive: {e}")

def csv_a_sqlite():
    """ Convierte un archivo CSV en una base de datos SQLite """
    if not os.path.exists(CSV_FILE):
        print("⚠️ No hay un archivo CSV disponible para convertir a SQLite.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS coordenadas")
    cursor.execute("""
        CREATE TABLE coordenadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            lat REAL,
            lng REAL
        )
    """)

    # Leer el archivo CSV y cargarlo en SQLite
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la primera fila de encabezados
        for row in reader:
            cursor.execute("INSERT INTO coordenadas (user_email, lat, lng) VALUES (?, ?, ?)", 
                           (row[0], float(row[1]), float(row[2])))

    conn.commit()
    conn.close()
    print("✅ Archivo CSV convertido a SQLite.")

def guardar_y_subir_coordenadas(user_email, coords):
    """ Guarda coordenadas en SQLite, sincroniza con CSV y las sube a Google Drive """
    guardar_en_sqlite(user_email, coords)
    subir_a_drive()
