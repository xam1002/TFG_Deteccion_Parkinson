const area = document.querySelector(".arrastrar");
const texto = area.querySelector("h2");
const input = area.querySelector("#archivo")

var archivoArrastrado;

document.getElementById("boton_p").addEventListener("click", (e) => {
    archivo = input.files;
    if (archivo[0] == undefined) {
        input.files = archivoArrastrado;
    }
});


area.querySelector("button").addEventListener("click", (e) => {
    input.click();
});

input.addEventListener("change", (e) => {
    archivo = input.files;
    area.classList.add("activo");
    area.classList.remove("activo");
    texto.textContent = "Vídeo " + archivo[0].name + " cargado";
});

area.addEventListener("dragover", (e) => {
    e.preventDefault();
    area.classList.add("activo");
    texto.textContent = "Suelte el vídeo aquí";
});

area.addEventListener("dragleave", (e) => {
    e.preventDefault();
    area.classList.remove("activo");
    texto.textContent = "Arrastre el vídeo para subirlo";
});

area.addEventListener("drop", (e) => {
    e.preventDefault();
    archivoArrastrado = e.dataTransfer.files;
    new FileReader().readAsDataURL(archivoArrastrado[0]);
    area.classList.remove("activo");
    texto.textContent = "Vídeo " + archivoArrastrado[0].name + " cargado";
});