import mysql.connector
from getpass import getpass
import hashlib

def conectar():
    mydb = mysql.connector.connect(
        host="localhost",
        user="Ashrah",
        password="GGWPYATMVP",
        database="turns"
    )
    return mydb

def registrar_usuario():
    username = input("Ingresa tu nombre de usuario: ")
    password = getpass("Ingresa tu contraseña: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    mydb = conectar()
    cursor = mydb.cursor()
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    val = (username, hashed_password)
    cursor.execute(sql, val)
    mydb.commit()
    print("Usuario registrado exitosamente")

def iniciar_sesion():
    username = input("Ingresa tu nombre de usuario: ")
    password = getpass("Ingresa tu contraseña: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    mydb = conectar()
    cursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, hashed_password)
    cursor.execute(sql, val)
    result = cursor.fetchall()

    if len(result) == 1:
        print("Inicio de sesión exitoso!")
    else:
        print("Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    opcion = input("¿Qué deseas hacer? (registrar/iniciar sesión): ")

    if opcion.lower() == "registrar":
        registrar_usuario()
    elif opcion.lower() == "iniciar sesión":
        iniciar_sesion()
    else:
        print("Opción inválida. Intenta nuevamente.")

# CAJ03UAL, SSE01UAL