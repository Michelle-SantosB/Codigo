import sqlite3       # Base de datos SQLite
import hashlib        # Hashing de contraseñas
from flask import Flask

# --- CONFIGURACIÓN ---
DB_NAME = "usuarios.db"

usuarios = {
    "Michelle": "Duoc.2025",
    "Branco": "Duoc.2025",
    "Jesus": "Duoc.2025"
}

# --- FLASK APP ---
app = Flask(__name__)

@app.route('/')
def inicio():
    return "Sitio web funcionando en el puerto 5800."

# --- CREAR BASE Y GUARDAR USUARIOS ---
def inicializar_base():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            nombre TEXT PRIMARY KEY,
            hash_contrasena TEXT
        )
    ''')
    conn.commit()
    conn.close()

def guardar_usuarios():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for nombre, clave in usuarios.items():
        hash_clave = hashlib.sha256(clave.encode()).hexdigest()
        cursor.execute("INSERT OR REPLACE INTO usuarios (nombre, hash_contrasena) VALUES (?, ?)", (nombre, hash_clave))
    conn.commit()
    conn.close()

# --- VALIDAR USUARIO ---
def validar_usuario(nombre, contrasena):
    hash_intento = hashlib.sha256(contrasena.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT hash_contrasena FROM usuarios WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    return fila and fila[0] == hash_intento

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == '__main__':
    inicializar_base()
    guardar_usuarios()

    # Mostrar hash de los usuarios
    for nombre, clave in usuarios.items():
        hash_clave = hashlib.sha256(clave.encode()).hexdigest()
        print(f"{nombre}: {hash_clave}")

    # Validar con input manual
    usuario_input = input("Ingrese su nombre: ")
    clave_input = input("Ingrese su contraseña: ")

    if validar_usuario(usuario_input, clave_input):
        print("Acceso concedido.")
    else:
        print("Usuario o contraseña incorrectos.")

    # Iniciar sitio web
    app.run(port=5800)
