document.getElementById('autoForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const rut = document.getElementById('rut').value;
    const telefono = document.getElementById('telefono').value;

    if (!validarRUT(rut)) {
        document.getElementById('rutError').textContent = 'RUT inválido';
    } else {
        document.getElementById('rutError').textContent = '';
    }

    if (!validarTelefono(telefono)) {
        document.getElementById('telefonoError').textContent = 'Teléfono inválido';
    } else {
        document.getElementById('telefonoError').textContent = '';
    }

    if (validarRUT(rut) && validarTelefono(telefono)) {
        alert('Formulario enviado correctamente');
    }
});

function validarRUT(rut) {
    const rutRegex = /^[0-9]+-[0-9Kk]$/;
    return rutRegex.test(rut);
}

function validarTelefono(telefono) {
    const telRegex = /^\+569[0-9]{8}$/;
    return telRegex.test(telefono);
}

function volver() {
    alert('Volver presionado');
}
/*  */
// Script para manejar el hover sobre las cartas de servicios
document.querySelectorAll('.servicio-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        // Cambiar el estilo o mostrar algo extra al pasar el mouse por encima
        this.querySelector('button').style.display = 'block';  // Muestra el botón al pasar el mouse
    });
    
    card.addEventListener('mouseleave', function() {
        // Ocultar el botón cuando se quita el mouse
        this.querySelector('button').style.display = 'none';
    });
});

// Este código es para asegurarse de que el modal se muestra correctamente
var modal = document.getElementById('modalServicio');
var modalInstance = new bootstrap.Modal(modal);

modal.addEventListener('shown.bs.modal', function () {
    console.log('El modal ha sido mostrado');
});

modal.addEventListener('hidden.bs.modal', function () {
    console.log('El modal ha sido cerrado');
});
/*  */

    // Función para manejar el registro de usuario
    function handleRegistration(event) {
        event.preventDefault();

        const nombre = event.target.nombre.value;
        const apellido = event.target.apellido.value;
        const correo = event.target.correo.value;
        const password = event.target.password.value;

        // Recuperar usuarios almacenados en localStorage
        const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

        // Verificar si el correo ya está registrado
        const usuarioExistente = usuarios.find(usuario => usuario.correo === correo);
        if (usuarioExistente) {
            // Mostrar error si el correo ya está registrado
            document.getElementById('registroError').innerText = 'El correo ya está registrado. Por favor, elija otro.';
            document.getElementById('registroError').style.display = 'block';
        } else {
            // Registrar al nuevo usuario en localStorage
            usuarios.push({ nombre, apellido, correo, password });
            localStorage.setItem('usuarios', JSON.stringify(usuarios));

            alert('Usuario registrado exitosamente!');
            window.location.href = 'login.html';  // Redirigir a la página de inicio de sesión
        }
    }

    // Función para manejar el inicio de sesión
    function handleLogin(event) {
        event.preventDefault();

        const correo = event.target.correo.value;
        const password = event.target.password.value;

        // Recuperar usuarios del localStorage
        const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
        const usuarioEncontrado = usuarios.find(usuario => usuario.correo === correo && usuario.password === password);

        if (usuarioEncontrado) {
            // Simulación de inicio de sesión exitoso
            alert('Inicio de sesión exitoso!');
            window.location.href = '/';  // Redirigir a la página principal
        } else {
            // Mostrar error si el usuario no existe o la contraseña es incorrecta
            document.getElementById('loginError').innerText = 'Correo o contraseña incorrectos.';
            document.getElementById('loginError').style.display = 'block';
        }
    }

    // Agregar los event listeners a los formularios
    document.addEventListener("DOMContentLoaded", function() {
        // Si estamos en la página de registro
        const registroForm = document.getElementById('registroForm');
        if (registroForm) {
            registroForm.addEventListener('submit', handleRegistration);
        }

        // Si estamos en la página de login
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', handleLogin);
        }
    });

