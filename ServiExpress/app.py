from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'clave_secreta'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 


servicios = [
    {"id": 1, "nombre": "Cambio de Aceite", "imagen": "static/images/cambioAceite.jpg"},
    {"id": 2, "nombre": "Revisión General", "imagen": "static/images/revisionGeneral.jpg"},
    {"id": 3, "nombre": "Alineación y Balanceo", "imagen": "static/images/alineacionBalanceo.jpg"},
    {"id": 4, "nombre": "Frenos", "imagen": "static/images/frenos.jpg"},
    {"id": 5, "nombre": "Cambio de Batería", "imagen": "static/images/cambioBateria.jpg"},
    {"id": 6, "nombre": "Cambio de Bujías", "imagen": "static/images/cambioBujias.jpg"},
]


usuarios = {"admin": "12345"}


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html', servicios=servicios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in usuarios and usuarios[username] == password:
            user = User(username)
            login_user(user)  # Iniciar sesión
            return redirect(url_for('index'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template('login.html')

@app.route('/servicio/<int:id>')
@login_required  
def servicio(id):
    servicio_seleccionado = next((s for s in servicios if s['id'] == id), None)
    if servicio_seleccionado:
        return render_template('servicio.html', servicio=servicio_seleccionado)
    else:
        return "Servicio no encontrado", 404

@app.route('/logout')
def logout():
    logout_user()  
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

