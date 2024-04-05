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
            host='127.0.0.1',
            database='cert',
            user='root'
        )
        if conexion.is_connected():
            print('Content-Type: text/html')  # Encabezado HTTP
            print()  # Línea en blanco que indica el final del encabezado HTTP
            print('<html><head><title>Registro</title></head><body>')  # Cuerpo de la respuesta HTML
            print('<h1>Conexión exitosa a la base de datos.</h1>')
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
        print(f"<p>Registro guardado exitosamente para {correo}</p>")
    except Error as e:
        print(f'<p>Error al guardar el registro: {e}</p>')
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
else:
    print('Content-Type: text/html')
    print()
    print('<html><head><title>Error</title></head><body>')
    print('<h1>Error: Debes proporcionar correo y contraseña.</h1>')
    print('</body></html>')
