class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'
    WTF_CSRF_SECRET_KEY = 'B2@reNAt1T^%kvhUI*S^'

class DevelopmentConfing(Config):
    DEBUG = True
    DEBUG_PROCESADO = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'flask_login'
    CARPETA_VIDEOS = '..//Flask//app//video'
    CARPETA_MODELOS = '..//Flask//app//modelo'

config = {
    'development': DevelopmentConfing,
}