from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Asegúrate de cambiar esto por algo más seguro

# Lista de usuarios con rol y datos adicionales
usuarios = [
    {'nombre': 'admin', 'apellido': 'admin', 'correo': 'admin@serviexpress.com', 'password': generate_password_hash('admin123'), 'rol': 'admin'},
    {'nombre': 'juan', 'apellido': 'perez', 'correo': 'juanperez@example.com', 'password': generate_password_hash('1234'), 'rol': 'cliente', 'auto': {'marca': 'Toyota', 'modelo': 'Corolla', 'anio': '2020', 'patente': 'ABC1234'}, 'servicios': [{'nombre': 'Cambio de Aceite', 'fecha': '2024-05-10', 'comentario': 'Excelente servicio'}], 'presupuestos': []},
    {'nombre': 'maria', 'apellido': 'lopez', 'correo': 'maria@example.com', 'password': generate_password_hash('5678'), 'rol': 'cliente', 'auto': {'marca': 'Honda', 'modelo': 'Civic', 'anio': '2021', 'patente': 'XYZ5678'}, 'servicios': [{'nombre': 'Alineación y Balanceo', 'fecha': '2024-06-15', 'comentario': 'Muy buena atención'}], 'presupuestos': []}
]

# Función para agregar un nuevo usuario
def agregar_usuario(nombre, apellido, correo, password, rol='cliente'):
    usuarios.append({'nombre': nombre, 'apellido': apellido, 'correo': correo, 'password': generate_password_hash(password), 'rol': rol})

# Ruta para la página principal ("/")
@app.route('/')
def index():
    usuario = session.get('usuario', None)  # Utilizar get para evitar KeyError
    return render_template('index.html', usuario=usuario)

# Ruta para el formulario de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        password = request.form['password']

        # Verificar si el correo ya está registrado
        for usuario in usuarios:
            if usuario['correo'] == correo:
                return jsonify({'success': False, 'message': 'El correo ya está registrado. Por favor, elija otro.'})

        # Si el correo no está registrado, agregamos al nuevo usuario
        agregar_usuario(nombre, apellido, correo, password)
        return jsonify({'success': True, 'message': 'Usuario registrado exitosamente!'})

    return render_template('registro.html')


# Ruta para el formulario de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        # Buscar el usuario en la lista
        for usuario in usuarios:
            if usuario['correo'] == correo and check_password_hash(usuario['password'], password):
                session['usuario'] = {'nombre': usuario['nombre'], 'rol': usuario['rol'], 'correo': usuario['correo']}  # Guardamos el nombre, rol y correo en la sesión
                return redirect(url_for('index'))  # Redirigir al inicio tras inicio de sesión exitoso

        return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos.'})

    return render_template('login.html')

# Ruta para la cuenta del cliente o admin
@app.route('/mi_cuenta', methods=['GET', 'POST'])
def cuenta():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    
    # Buscar los detalles del usuario desde la lista
    cliente = next(u for u in usuarios if u['correo'] == usuario['correo'])
    
    if usuario['rol'] == 'admin':
        # Si es admin, renderizamos el template de cuenta_admin.html
        return render_template('cuenta_admin.html', usuario=usuario, clientes=usuarios, rol=usuario['rol'])

    # Si es cliente, renderizamos el template de cuenta.html
    servicios_realizados = cliente.get('servicios', [])
    presupuestos = cliente.get('presupuestos', [])
    auto = cliente.get('auto', {})

    if request.method == 'POST':
        # Actualizar los datos del cliente si se hace un POST
        cliente['nombre'] = request.form['nombre']
        cliente['correo'] = request.form['correo']

        return redirect(url_for('cuenta'))

    return render_template('cuenta.html', usuario=cliente, servicios_realizados=servicios_realizados, presupuestos=presupuestos, auto=auto, rol=usuario['rol'])

# Ruta para el registro de servicio
@app.route('/registroServicio', methods=['GET', 'POST'])
def registroServicio():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Simular la creación de un servicio para el usuario
        usuario = session['usuario']
        servicio = {
            'nombre': request.form['nombre'],
            'fecha': request.form['fecha'],
            'comentario': request.form['comentario']
        }

        # Buscar al cliente en la lista
        cliente = next(u for u in usuarios if u['correo'] == usuario['correo'])
        cliente['servicios'].append(servicio)
        return redirect(url_for('cuenta'))

    return render_template('registroServicio.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar la información de la sesión
    session.pop('usuario', None)
    return redirect(url_for('index'))  # Redirigir al inicio después de cerrar sesión

if __name__ == '__main__':
    app.run(debug=True)

