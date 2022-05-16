function confirmacion(e) {
    if (!confirm("¿Está seguro que desea eliminar el usuario?"))
        e.preventDefault();
}