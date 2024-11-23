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