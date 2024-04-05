#!/usr/bin/env python3
import cgi
import cgitb
import mysql.connector
from mysql.connector import Error

# Activa el modo de depuración para ver los errores en el navegador
cgitb.enable()

# Función para conectar a la base de datos MySQL
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='127.0.0.1:33065',
            database='cert',
            user='root'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print('Content-Type: text/html')
        print()
        print('<html><head><title>Error</title></head><body>')
        print(f'<h1>Error al conectar a la base de datos: {e}</h1>')
        print('</body></html>')

# Función para guardar registro en la base de datos
def guardar_registro(correo, contraseña):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO usuarios (correo, contraseña) VALUES (%s, %s)"
        val = (correo, contraseña)
        cursor.execute(sql, val)
        conexion.commit()
        print(f"Registro guardado exitosamente para {correo}")
    except Error as e:
        print(f'Error al guardar el registro: {e}')
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Procesar datos enviados desde el formulario
form = cgi.FieldStorage()
correo = form.getvalue('correo')
contraseña = form.getvalue('contraseña')

# Guardar registro si se enviaron datos desde el formulario
if correo and contraseña:
    guardar_registro(correo, contraseña)
    print('Content-Type: text/html')
    print()
    print('<html><head><title>Registro Exitoso</title></head><body>')
    print('<h1>Registro exitoso</h1>')
    print('</body></html>')
else:
    print('Content-Type: text/html')
    print()
    print('<html><head><title>Error</title></head><body>')
    print('<h1>Error: Debes proporcionar correo y contraseña.</h1>')
    print('</body></html>')
