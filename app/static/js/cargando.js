function cargando() {
    // var mano = document.getElementById('mano');
    // var sexo = document.getElementById('sexo');
    // manoSeleccionada = mano.options[mano.selectedIndex];
    // sexoSeleccionado = mano.options[sexo.selectedIndex];
    // if (manoSeleccionada.value != "" && sexoSeleccionado.value != "") {
        var contenedor = document.getElementById('contenedor_carga');
        var bienvenida = document.getElementById('bienvenida');
        var subida = document.getElementById('subida');
        contenedor.style.visibility = 'visible';
        contenedor.style.opacity = '1';
        bienvenida.style.visibility = 'hidden';
        bienvenida.style.opacity = '0';
        subida.style.visibility = 'hidden';
        subida.style.opacity = '0';
    // }
}