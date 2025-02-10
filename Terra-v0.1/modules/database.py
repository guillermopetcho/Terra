import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../users.db")

def crear_tabla_usuarios():
    """Crea la tabla de usuarios si no existe"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                imagen TEXT
            )
        """)
        conn.commit()

def usuario_existe(email):
    """Verifica si un usuario ya existe en la base de datos"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        return cursor.fetchone() is not None

def guardar_usuario(id, nombre, email, imagen):
    """Guarda un nuevo usuario en la base de datos"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (id, nombre, email, imagen) VALUES (?, ?, ?, ?)", 
                       (id, nombre, email, imagen))
        conn.commit()

# Crear la tabla al iniciar
crear_tabla_usuarios()
