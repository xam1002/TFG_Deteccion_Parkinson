import os

class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'
    WTF_CSRF_SECRET_KEY = 'B2@reNAt1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_PROCESADO = True
    HOST = 'localhost'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'flask_bd'
    CARPETA_VIDEOS = os.path.join('..', 'app', 'video')
    CARPETA_MODELOS = os.path.join('..', 'app', 'modelo')

config = {
    'development': DevelopmentConfig,
}
