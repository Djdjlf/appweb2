import tkinter as tk
from tkinter import messagebox
import sqlite3
import smtplib
import webbrowser

# Función para enviar un correo electrónico
def enviar_correo(correo_destino):
    # Configuración del servidor SMTP (en este caso usaremos Gmail)
    servidor_smtp = "smtp.gmail.com"
    puerto = 587  # Puerto TLS

    # Dirección de correo electrónico y contraseña de la cuenta que enviará el correo
    correo_emisor = "pruebasdelaappweb@gmail.com"  # ¡Reemplaza con tu dirección de correo!
    contraseña_emisor = "Angel1931?"    # ¡Reemplaza con tu contraseña!

    # Configurar el servidor SMTP
    servidor = smtplib.SMTP(servidor_smtp, puerto)
    servidor.starttls()  # Iniciar conexión TLS
    servidor.login(correo_emisor, contraseña_emisor)

    # Construir el mensaje
    asunto = "Registro exitoso"
    mensaje = "Hola,\n\nTu registro en nuestra aplicación fue exitoso.\n\nSaludos"
    mensaje_final = f"Subject: {asunto}\n\n{mensaje}"

    # Enviar el correo electrónico
    servidor.sendmail(correo_emisor, correo_destino, mensaje_final)

    # Cerrar la conexión con el servidor SMTP
    servidor.quit()

# Función para registrar un nuevo usuario en la base de datos
def registrar_usuario():
    nombre_usuario = entrada_usuario.get()
    correo = entrada_correo.get()
    contraseña = entrada_contraseña.get()

    # Verificar si los campos están completos
    if nombre_usuario and correo and contraseña:
        # Conectar a la base de datos SQLite (si no existe, se creará)
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        # Crear la tabla de usuarios si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                          (nombre_usuario TEXT PRIMARY KEY, correo TEXT UNIQUE, contraseña TEXT)''')

        try:
            # Insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?)", (nombre_usuario, correo, contraseña))
            conexion.commit()

            # Enviar correo electrónico de confirmación
            enviar_correo(correo)

            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", "El correo o el nombre de usuario ya están en uso")
            else:
                messagebox.showerror("Error", "Error al registrar el usuario")
        finally:
            conexion.close()
    else:
        messagebox.showwarning("Advertencia", "Por favor ingresa todos los datos")

# Función para iniciar sesión
def iniciar_sesion():
    correo = entrada_correo.get()
    contraseña = entrada_contraseña.get()

    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    # Buscar el usuario en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
    usuario = cursor.fetchone()

    if usuario:
        if usuario[2] == contraseña:
            messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {usuario[0]}!")
            # Abrir una URL personalizada en el navegador
            webbrowser.open("https://www.facebook.com")  # ¡Reemplaza con tu URL!
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        messagebox.showerror("Error", "Correo electrónico no encontrado")

    conexion.close()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Aplicación de Registro y Login")
ventana.geometry("300x250")

# Crear un marco para el menú de login
marco_login = tk.LabelFrame(ventana, text="Login")
marco_login.pack(pady=20)

# Etiqueta y entrada para el nombre de usuario
etiqueta_usuario = tk.Label(marco_login, text="Nombre de usuario:")
etiqueta_usuario.grid(row=0, column=0, padx=5, pady=5)
entrada_usuario = tk.Entry(marco_login)
entrada_usuario.grid(row=0, column=1, padx=5, pady=5)

# Etiqueta y entrada para el correo electrónico
etiqueta_correo = tk.Label(marco_login, text="Correo electrónico:")
etiqueta_correo.grid(row=1, column=0, padx=5, pady=5)
entrada_correo = tk.Entry(marco_login)
entrada_correo.grid(row=1, column=1, padx=5, pady=5)

# Etiqueta y entrada para la contraseña
etiqueta_contraseña = tk.Label(marco_login, text="Contraseña:")
etiqueta_contraseña.grid(row=2, column=0, padx=5, pady=5)
entrada_contraseña = tk.Entry(marco_login, show="*")
entrada_contraseña.grid(row=2, column=1, padx=5, pady=5)

# Botón para iniciar sesión
boton_login = tk.Button(marco_login, text="Iniciar sesión", command=iniciar_sesion)
boton_login.grid(row=3, columnspan=2, padx=5, pady=5, sticky="ew")

# Botón para registrar un nuevo usuario
boton_registro = tk.Button(marco_login, text="Registrarse", command=registrar_usuario)
boton_registro.grid(row=4, columnspan=2, padx=5, pady=5, sticky="ew")

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
