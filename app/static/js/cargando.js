/**
 * Implementa la función para que aparezca el símbolo de cargando al realizar una predicción.
 */
function cargando() {
    const area = document.querySelector(".arrastrar");
    const input = area.querySelector("#archivo");
    var mano = document.predecir.mano;
    var sexo = document.predecir.sexo;
    var archivo = document.predecir.archivo;
    console.log(input.files);
    extensiones = [".ogm", ".wmv", ".mpg", ".webm", ".ogv", ".mov", ".asx", ".mpeg", ".mp4", ".m4v", ".avi", ".mkv"]
    if (mano.value != '' && sexo.value != '' && (archivo.value != '' && !extensiones.includes(archivo.value) 
    || input.files != '' && !extensiones.includes(input.files))) {
        var contenedor = document.getElementById('contenedor_carga');
        var bienvenida = document.getElementById('bienvenida');
        var subida = document.getElementById('subida');
        contenedor.style.display = 'block';
        bienvenida.style.visibility = 'hidden';
        bienvenida.style.opacity = '0';
        subida.style.visibility = 'hidden';
    }
}
