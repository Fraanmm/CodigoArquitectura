from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Asegúrate de cambiar esto por algo más seguro

# Función para conectarse a la base de datos y agregar un nuevo usuario
def agregar_usuario(nombre, apellido, correo, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)  # Encriptamos la contraseña
    cursor.execute('''
    INSERT INTO usuarios (nombre, apellido, correo, password)
    VALUES (?, ?, ?, ?)
    ''', (nombre, apellido, correo, hashed_password))
    conn.commit()
    conn.close()

# Ruta para la página principal ("/")
@app.route('/')
def index():
    if 'usuario' in session:
        return render_template('index.html', usuario=session['usuario'])
    return render_template('index.html')

# Ruta para el formulario de registro y manejo de la solicitud POST
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        password = request.form['password']

        try:
            # Conectar a la base de datos y verificar si el correo ya está registrado
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                conn.close()
                return jsonify({'success': False, 'message': 'El correo ya está registrado. Por favor, elija otro.'})

            # Si el correo no está registrado, agregamos al nuevo usuario
            agregar_usuario(nombre, apellido, correo, password)
            conn.close()

            # Retornar respuesta exitosa
            return jsonify({'success': True, 'message': 'Usuario registrado exitosamente!'})

        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': f'Error al registrar el usuario: {str(e)}'})

    return render_template('registro.html')

# Ruta para el formulario de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        try:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,))
            usuario = cursor.fetchone()
            conn.close()

            if usuario and check_password_hash(usuario[4], password):  # Verificamos la contraseña encriptada
                session['usuario'] = usuario[1]  # Guardamos el nombre del usuario en la sesión
                return jsonify({'success': True, 'message': 'Inicio de sesión exitoso!'})
            else:
                return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos.'})

        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al procesar el inicio de sesión: {str(e)}'})

    return render_template('login.html')

# Ruta para el registro de servicio
@app.route('/registroServicio')
def registroServicio():
    return render_template('registroServicio.html')

@app.route('/mi_cuenta', methods=['GET', 'POST'])
def cuenta():
    if 'usuario' not in session:
        return redirect(url_for('login'))

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

    if request.method == 'POST':
        usuario['nombre'] = request.form['nombre']
        usuario['correo'] = request.form['correo']
        usuario['datos_bancarios'] = request.form['datos_bancarios']
        usuario['marca_auto'] = request.form['marca_auto']
        usuario['modelo_auto'] = request.form['modelo_auto']
        usuario['anio_auto'] = request.form['anio_auto']
        usuario['patente_auto'] = request.form['patente_auto']

        return redirect(url_for('cuenta'))

    return render_template('mi_cuenta.html', usuario=usuario, servicios_realizados=servicios_realizados)

if __name__ == '__main__':
    app.run(debug=True)



