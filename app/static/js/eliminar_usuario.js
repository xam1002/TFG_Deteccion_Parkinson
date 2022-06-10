/**
 * Implementa la ventana de confirmación para eliminar un usuario.
 * @param e Evento.
 */
function confirmacion(e) {
    if (!confirm("¿Está seguro que desea eliminar el usuario?"))
        e.preventDefault();
}
