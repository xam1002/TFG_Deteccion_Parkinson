# Autor: Álvaro Alonso Marín


# Importación de bibliotecas
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self, id, nombre, contraseña, nombre_completo="") -> None:
        '''
        Constructor de la clase.

        Parámetros:
        - id: identificador del usuario.
        - nombre: nombre del usuario.
        - contraseña: contraseña del usuario.
        - nombre_completo: nombre completo del usuario.
        '''
        self.id = id
        self.nombre = nombre
        self.contraseña = contraseña
        self.nombre_completo = nombre_completo

    @classmethod
    def verificar_clave(self, contraseña_hash, contraseña):
        '''
        Comprueba si la clave introducida en el inicio de sesión es correcta.

        Parámetros:
        - contraseña_hash: contraseña verdadera del usuario.
        - contraseña: contraseña introducida.

        Retorno:
        - True si la contraseña es correcta y False si no lo es.
        '''
        return check_password_hash(contraseña_hash, contraseña)
    
    @classmethod
    def iniciar_sesion(self, conexion, usuario):
        '''
        Inicia sesión con el usuario.

        Parámetros:
        - conexion: conexión con la base de datos.
        - usuario: usuario que inicia sesión.

        Retorno:
        - El usuario si el usuario existe, si no retorna None.
        '''
        try:
            cursor=conexion.connection.cursor()
            sql="""SELECT id, usuario, contraseña, nombre_completo FROM usuarios 
                    WHERE usuario = '{}'""".format(usuario.nombre)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
               return self(row[0], row[1], self.verificar_clave(row[2], usuario.contraseña), row[3])
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_por_id(self, conexion, id):
        '''
        Obtiene el usuario con el id pasado por parámetro.

        Parámetros:
        - conexion: conexión con la base de datos.
        - id: identificador del usuario.

        Retorno:
        - El usuario si el usuario existe, si no retorna None.
        '''
        try:
            cursor=conexion.connection.cursor()
            sql="SELECT id, usuario, nombre_completo FROM usuarios WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
               return self(row[0], row[1], None, row[2])
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_id(self, conexion):
        '''
        Obtiene el id más bajo disponible.

        Parámetros:
        - conexion: conexión con la base de datos.

        Retorno:
        - El id más bajo disponible.
        '''
        try:
            i = 0
            cursor=conexion.connection.cursor()
            sql="""SELECT id FROM usuarios ORDER BY id ASC"""
            cursor.execute(sql)
            row = cursor.fetchone()
            while row is not None and row[0] == i:
                row = cursor.fetchone()
                i+=1
            return i
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def existe_usuario(self, conexion, id, nombre):
        '''
        Comprueba si el usuario existe.

        Parámetros:
        - conexion: conexión con la base de datos.
        - id: identificador del usuario.
        - nombre: nombre del usuario.

        Retorno:
        - True si el usuario existe y Flase si no.
        '''
        try:
            cursor=conexion.connection.cursor()
            if id == -1:
                sql="""SELECT usuario FROM usuarios WHERE usuario = '{}'""".format(nombre)
            else:
                sql="""SELECT usuario FROM usuarios WHERE id != '{}' AND usuario = '{}'""".format(id, nombre)
            cursor.execute(sql)
            return cursor.fetchone() != None
        except Exception as ex:
            raise Exception(ex)
