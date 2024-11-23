from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Asegúrate de cambiar esto a algo más seguro en producción

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        # Lógica para verificar las credenciales en la base de datos
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE correo=? AND password=?', (correo, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for('cuenta'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Ruta de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        password = request.form['password']

        # Guardar en la base de datos
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, apellido, correo, password) VALUES (?, ?, ?, ?)', 
                       (nombre, apellido, correo, password))
        conn.commit()
        conn.close()

        flash('Registro exitoso, por favor inicie sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

# Ruta para mostrar la cuenta del usuario
@app.route('/cuenta', methods=['GET', 'POST'])
def cuenta():
    if request.method == 'POST':
        # Aquí puedes implementar lógica para actualizar la cuenta
        pass

    return render_template('cuenta.html')

# Ruta para registrar un servicio
@app.route('/registroServicios', methods=['GET', 'POST'])
def registro_servicios():
    if request.method == 'POST':
        # Lógica para registrar el servicio
        pass
    return render_template('registroServicios.html')

if __name__ == '__main__':
    app.run(debug=True)




