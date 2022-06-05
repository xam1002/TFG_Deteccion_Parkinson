# Aplicación web que recibe las peticiones y renderiza las plantillas correspondientes.
# Autor: Álvaro Alonso Marín

# Importación de bibliotecas
from attr import Attribute
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from impl.Gestion_usuarios import Gestion_usuarios
from config import config
from impl.Usuario import Usuario
from impl.Procesado import Procesado
from werkzeug.exceptions import BadRequestKeyError
import os
import glob

# Instanciación de atributos globales
app = Flask(__name__)
conexion = MySQL(app)
login_manager_app = LoginManager(app)
csrf = CSRFProtect()

@login_manager_app.user_loader
def load_user(id):
    '''
    Se obtiene el usuario que ha iniciado sesión.

    Parámetros:
    - id: identificador del usuario.

    Retorno:
    - Usuario que ha iniciado sesión.
    '''
    return Usuario.obtener_por_id(conexion, id)

@app.route('/')
def index():
    '''
    Redirige las peticiones de la URL raíz al inicio de sesión.

    Retorno:
    - Redirección de la petición al inicio de sesión.
    '''
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Valida el inicio de sesión del usuario.

    Retorno:
    - Si el usuario es el admin, se redirige al usuario a la ventana de inicio de admin.
    - Si el usuario no es el admin, se redirige al usuario a la ventana de inicio de usuario.
    - Si el usuario o la contraseña no son válidos, se redirige de nuevo al inicio de sesión.
    '''
    if request.method=='POST':
        user = Usuario(0, request.form['username'], request.form['password'])
        logged_user = Usuario.iniciar_sesion(conexion, user)
        if logged_user != None:
            if logged_user.contraseña:
                login_user(logged_user)
                if request.form['username'] == 'admin':
                    return  redirect(url_for('admin'))
                return redirect(url_for('upload'))
            else:
                flash("Contraseña inválida...")
        else:
            flash("Usuario no encontrado...")
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    '''
    Desconecta al usuario actual y redirige la petición a la pantalla de inicio de sesión.

    Retorno:
    - Redirección a la ventana de inicio de sesión.
    '''
    logout_user()
    return redirect(url_for('login'))

@app.route('/gestion_usuarios')
@login_required
def gestion_usuarios():
    '''
    Muestra la ventana de la gestión de usuarios si el usuario actual es el admin y lista los usuarios
    dados de alta en la aplicación.

    Retorno:
    - Si el usuario es el admin, se redirige al usuario a la ventana de gestión de usuarios.
    - Si el usuario no es el admin, se redirige al usuario a la ventana inicial.
    '''
    if current_user.nombre == 'admin':
        data = {'usuarios': Gestion_usuarios.obtener_usuarios(conexion)}
        return render_template('admin/gestion_usuarios.html', data=data)
    return redirect(url_for('upload'))

@app.route('/agregar_usuario')
@login_required
def agregar_usuario():
    '''
    Muestra la ventana para añadir usuarios si el usuario actual es el admin.

    Retorno:
    - Si el usuario es el admin, se redirige al usuario a la ventana de alta de usuarios.
    - Si el usuario no es el admin, se redirige al usuario a la ventana inicial.
    '''
    if current_user.nombre == 'admin':
        return render_template('admin/agregar_usuario.html')
    return redirect(url_for('upload'))

@app.route('/usuario_agregado', methods=['POST'])
@login_required
@csrf.exempt
def usuario_agregado():
    '''
    Se realiza el alta del usuario con los datos de la petición y regresa a la ventana de gestión
    de usuarios.

    Retorno:
    - Si el usuario es el admin, se realiza el alta del usuario y se redirige a la ventana de 
      gestión de usuarios.
    - Si el usuario no es el admin, se redirige al usuario a la ventana de inicio de usuario.
    - Si el usuario ya existe o las contraseñas no coinciden, se redirige de nuevo al alta del 
      usuario.
    '''
    if current_user.nombre == 'admin':
        if request.method == 'POST':
            nombre_completo = request.form['nombre_completo']
            nombre = request.form['nombre']
            contraseña = request.form['contraseña']
            if Usuario.existe_usuario(conexion, -1, nombre):
                flash("El usuario ya existe...")
                return render_template('admin/agregar_usuario.html')
            if request.form['contraseña'] != request.form['confirmar_contraseña']:
                flash("Las contraseñas no coinciden...")
                return redirect(url_for('agregar_usuario'))
            Gestion_usuarios.agregar_usuario(conexion, nombre, contraseña, nombre_completo)
        return redirect(url_for('gestion_usuarios'))
    return redirect(url_for('upload'))

@app.route('/modificar_usuario/<int:id>')
@login_required
def modificar_usuario(id):
    '''
    Muestra la ventana para modificar un usuario si el usuario actual es el admin.

    Parámetros:
    - id: identificador del usuario que se quiere modificar.

    Retorno:
    - Si el usuario es el admin, se redirige al usuario a la ventana de modificación de usuarios.
    - Si el usuario no es el admin, se redirige al usuario a la ventana inicial.
    '''
    data={'usuario': Gestion_usuarios.mostrar_datos_usuario(conexion, id), 'id': id}
    return render_template('modificar_usuario.html', data=data)

@app.route('/usuario_modificado/<int:id>', methods=['POST'])
@login_required
@csrf.exempt
def usuario_modificado(id):
    '''
    Se realiza la modificación del usuario con los datos de la petición y regresa a la ventana de gestión
    de usuarios.

    Parámetros:
    - id: identificador del usuario que se va a modificar.

    Retorno:
    - Si el usuario es el admin, se realiza la modificación del usuario y se redirige a la ventana de 
      gestión de usuarios.
    - Si el usuario no es el admin, se redirige al usuario a la ventana de inicio de usuario.
    - Si el usuario ya existe o las contraseñas no coinciden, se redirige de nuevo a la modificación 
      del usuario.
    '''
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        if Usuario.existe_usuario(conexion, id, nombre):
            flash("El usuario ya existe...")
            return redirect(url_for('modificar_usuario', id=id))
        if request.form['contraseña'] != request.form['confirmar_contraseña']:
            flash("Las contraseñas no coinciden...")
            return redirect(url_for('modificar_usuario', id=id))
        Gestion_usuarios.modificar_usuario(conexion, nombre, contraseña, nombre_completo, id)
    return redirect(url_for('gestion_usuarios'))

@app.route('/usuario_borrado/<int:id>')
@login_required
def usuario_borrado(id):
    '''
    Se realiza la eliminación del usuario y regresa a la ventana de gestión de usuarios.

    Parámetros: 
    - id: identificador del usuario que se desea borrar.

    Retorno:
    - Si el usuario es el admin, se realiza la eliminación del usuario y se redirige a la ventana de 
      gestión de usuarios.
    - Si el usuario no es el admin, se redirige al usuario a la ventana de inicio de usuario.
    '''
    if current_user.nombre == 'admin':
        if request.method == 'GET':
            Gestion_usuarios.eliminar_usuario(conexion, id)
        return redirect(url_for('gestion_usuarios'))
    return redirect(url_for('upload'))

@app.route('/upload')
@login_required
def upload():
    '''
    Renderiza la plantilla que contiene la pantalla inicial de un usuario sin privilegios.

    Retorno:
    - Plantilla de la pantalla inicial renderizada.
    '''
    return render_template('pred/archivos.html')

@app.route('/admin')
@login_required
def admin():
    '''
    Renderiza la plantilla que contiene la pantalla inicial de un usuario con privilegios.

    Retorno:
    - Si el usuario es el admin, se retorna la plantilla de la pantalla inicial renderizada.
    - Si el usuario no es el admin, se redirige al usuario a la ventana de inicio de usuario.
    '''
    if current_user.nombre == 'admin':
        return render_template('admin/archivos_admin.html')
    return redirect(url_for('upload'))

@app.route('/uploader', methods=['POST'])
@login_required
@csrf.exempt
def uploader():
    '''
    Sube el vídeo junto a los datos al servidor y realiza la predicción.

    Retorno:
    - Plantilla renderizada con la predicción realizada.
    '''
    if request.method == 'POST':
        try:
            extensiones = [".ogm", ".wmv", ".mpg", ".webm", ".ogv", ".mov", ".asx", ".mpeg", ".mp4", ".m4v", ".avi"]
            f = request.files['archivo']
            filename = secure_filename(f.filename)
            mano = request.form['mano']
            sexo = request.form['sexo']
            if os.path.splitext(filename)[1] not in extensiones:
                flash("Archivo no válido...")
                return redirect(url_for('admin'))
            f.save(os.path.join(app.config['CARPETA_VIDEOS'], filename))
            prediccion = Procesado.realizar_prediccion(app.config['CARPETA_VIDEOS']+"//"+filename, mano, sexo, app.config['DEBUG_PROCESADO'])
            os.remove(app.config['CARPETA_VIDEOS']+"//"+filename)
        except BadRequestKeyError:
            flash("Se deben rellenar todos los campos...")
            if current_user.nombre == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('upload'))

    return render_template('pred/prediccion.html', data = {'prediccion': round(prediccion[0][1], 4)})

@app.route('/modificar_modelo')
@login_required
def modificar_modelo():
    '''
    Muestra la ventana para modificar el modelo si el usuario actual es el admin.

    Retorno:
    - Si el usuario es el admin, se redirige al usuario a la ventana para modificar el modelo.
    - Si el usuario no es el admin, se redirige al usuario a la ventana inicial.
    '''
    if current_user.nombre == 'admin':
        return render_template('admin/modificar_modelo.html')
    return redirect(url_for('upload'))

@app.route('/subida_modelo', methods=['POST'])
@login_required
@csrf.exempt
def subida_modelo():
    '''
    Sube el modelo actualizado al servidor.

    Retorno:
    - Si el usuario es el admin, se retorna la plantilla renderizada con la confirmación de que
      el modelo se ha actualizado.
    - Si el usuario no es el admin, se redirige al usuario a la ventana de inicio de usuario.
    '''
    if current_user.nombre == 'admin':
        if request.method == 'POST':
            f = request.files['archivo']
            filename = secure_filename(f.filename)
            if os.path.splitext(filename)[1] != '.pkl':
                flash("Archivo no válido...")
                return redirect(url_for('modificar_modelo'))
            for g in glob.glob('..//Flask//app//modelo//*'):
                os.remove(g)
            f.save(os.path.join(app.config['CARPETA_MODELOS'], filename))
        return render_template('admin/modelo_actualizado.html')
    return redirect(url_for('upload'))

def pagina_no_accesible(error):
    '''
    Redirige las peticiones de accesos restringidos a la pantalla de inicio de seisón.

    Parámetros:
    - error: tipo de error

    Retorno:
    - Redirección a la pantalla de inicio de sesión.
    '''
    return redirect(url_for('login'))

def pagina_no_encontrada(error):
    '''
    Redirige las peticiones de URLs inexistentes a una pantalla de error.

    Parámetros:
    - error: tipo de error.

    Retorno:
    - Plantilla renderizada con mensaje de error.
    '''
    try:
        current_user.nombre
    except AttributeError:
        return redirect(url_for('login'))
    return render_template('404.html'), 404

def pagina_no_permitida(error):
    '''
    Redirige las peticiones con métodos no permitidos al inicio.

    Parámetros:
    - error: tipo de error.

    Retorno:
    - Redirección a la pantalla inicial.
    '''
    try: 
        if current_user.nombre == 'admin':
            return redirect(url_for('admin'))
        return redirect(url_for('upload'))
    except AttributeError:
        return redirect(url_for('login'))

# Método raíz
if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, pagina_no_accesible)
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(405, pagina_no_permitida)
    app.run(host=app.config['HOST'], debug=True)
 
