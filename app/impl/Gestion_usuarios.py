# Autor: Álvaro Alonso Marín


# Importación de bibliotecas
from werkzeug.security import generate_password_hash
from impl.Usuario import Usuario

'''
Implementa los métodos de la gestión de usuarios.
'''
class Gestion_usuarios():

    @classmethod
    def obtener_usuarios(self, conexion):
        '''
        Obtiene los usuarios dados de alta en la aplicación.

        Parámetros:
        - conexion: conexión con la base de datos.

        Retorno:
        - Usuarios dados de alta en la apliación.
        '''
        try:
            cursor=conexion.connection.cursor()
            sql="SELECT nombre_completo, id FROM usuarios"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregar_usuario(self, conexion, nombre, contraseña, nombre_completo):
        '''
        Añade un usuario a la aplicación.

        Parámetros:
        - conexion: conexión con la base de datos.
        - nombre: nombre del usuario que se desea agregar.
        - contraseña: contraseña del usuario que se desea agregar.
        - nombre_completo: nombre completo del usuario que se desea agregar.
        '''
        try:
            cursor=conexion.connection.cursor()
            contraseña_hash = generate_password_hash(contraseña)
            sql="""INSERT INTO usuarios (id, usuario, contraseña, nombre_completo) 
                VALUES ('{}', '{}', '{}', '{}');
                """.format(Usuario.obtener_id(conexion), nombre, contraseña_hash, nombre_completo)
            cursor.execute(sql)
            conexion.connection.commit()
        except Exception as ex:
            raise ex

    @classmethod
    def mostrar_datos_usuario(self, conexion, id):
        '''
        Obtiene los datos de un usuario existente.

        Parámetros:
        - conexion: conexión con la base de datos.
        - id: identificador del usuario del que se desea obtener los datos.

        Retorno:
        - El nombre completo y el nombre del usuario.
        '''
        try:
            cursor=conexion.connection.cursor()
            sql="SELECT nombre_completo, usuario FROM usuarios WHERE id = '{}'".format(id)
            cursor.execute(sql)
            return cursor.fetchall()[0]
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def modificar_usuario(self, conexion, nombre, contraseña, nombre_completo, id):
        '''
        Realiza la modificación del usuario.

        Parámetros:
        - conexion: conexión con la base de datos.
        - nombre: nombre del usuario que se desea modificar.
        - contraseña: contraseña del usuario que se desea modificar.
        - nombre_completo: nombre completo del usuario que se desea modificar.
        - id: identificador del usuario que se desea modificar.
        '''
        try:
            cursor=conexion.connection.cursor()
            contraseña_hash = generate_password_hash(contraseña)
            sql="""UPDATE usuarios SET usuario='{}', contraseña='{}', nombre_completo='{}' 
                WHERE id = '{}'""".format(nombre, contraseña_hash, nombre_completo, id)
            cursor.execute(sql)
            conexion.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def eliminar_usuario(self, conexion, id):
        try:
            cursor=conexion.connection.cursor()
            sql="""DELETE FROM usuarios WHERE id = '{}'""".format(id)
            cursor.execute(sql)
            conexion.connection.commit()
        except Exception as ex:
            raise ex
