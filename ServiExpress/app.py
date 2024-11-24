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

# Ruta para el registro de servicio
@app.route('/registroServicio')
def registroServicio():
    # Aquí va la lógica para manejar el registro del servicio
    return render_template('registroServicio.html')  # O la plantilla que necesites

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/mi_cuenta', methods=['GET', 'POST'])
def cuenta():
    # Simulando obtener datos del usuario y los servicios realizados de una base de datos
    usuario = {
        'nombre': 'Juan Perez',
        'correo': 'juanperez@example.com',
        'datos_bancarios': 'Cuenta corriente 1234',
        'marca_auto': 'Toyota',
        'modelo_auto': 'Corolla',
        'anio_auto': '2020',
        'patente_auto': 'ABC1234'
    }
    
    servicios_realizados = [
        {'nombre': 'Cambio de Aceite', 'fecha': '2024-05-10'},
        {'nombre': 'Alineación y Balanceo', 'fecha': '2024-06-15'},
    ]

    # Si el método es POST, actualizamos los datos (esto es solo un ejemplo)
    if request.method == 'POST':
        usuario['nombre'] = request.form['nombre']
        usuario['correo'] = request.form['correo']
        usuario['datos_bancarios'] = request.form['datos_bancarios']
        usuario['marca_auto'] = request.form['marca_auto']
        usuario['modelo_auto'] = request.form['modelo_auto']
        usuario['anio_auto'] = request.form['anio_auto']
        usuario['patente_auto'] = request.form['patente_auto']
        # Guardar los cambios en la base de datos, etc.

        # Redirigir o mostrar un mensaje de éxito
        return redirect(url_for('cuenta'))

    return render_template('mi_cuenta.html', usuario=usuario, servicios_realizados=servicios_realizados)
