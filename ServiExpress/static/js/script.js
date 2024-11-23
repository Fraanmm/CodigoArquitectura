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