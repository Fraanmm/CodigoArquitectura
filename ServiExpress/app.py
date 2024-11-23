from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para conectarse a la base de datos y agregar un nuevo usuario
def agregar_usuario(nombre, apellido, correo, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO usuarios (nombre, apellido, correo, password)
    VALUES (?, ?, ?, ?)
    ''', (nombre, apellido, correo, password))
    conn.commit()
    conn.close()

# Ruta para la página principal ("/")
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza el archivo index.html

# Ruta para el formulario de registro y manejo de la solicitud POST
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        password = request.form['password']

        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,))
        usuario_existente = cursor.fetchone()
        conn.close()

        if usuario_existente:
            return "El correo ya está registrado. Por favor, elija otro."

        agregar_usuario(nombre, apellido, correo, password)
        return redirect(url_for('login'))  # Redirige al login después de registrar

    return render_template('registro.html')

# Ruta para el formulario de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE correo = ? AND password = ?', (correo, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return "Inicio de sesión exitoso!"
        else:
            return "Correo o contraseña incorrectos."

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)


