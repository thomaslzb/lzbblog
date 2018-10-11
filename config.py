import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'this is secret string'
    #SECRET_KEY = a-really-long-and-unique-key-that-nobody-knows
    """
    # Sqlite Database
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' +  os.path.join(basedir, 'app.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    """
    """
        Connect MySQL
    """
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'app' # DataBase Name
    USERNAME = 'root'
    PASSWORD = 'root'
    DB_URI = 'mysql+cymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI       # 这个参数是SQLAlchemy 内部定义的参数
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 这个参数是SQLAlchemy 内部定义的参数

    """
        Define Mail Servers
        MAIL_SERVER = os.environ.get('MAIL_SERVER')
        MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
        MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        ADMINS = ['your-email@example.com']
    """
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'thomaslzbuk'
    MAIL_PASSWORD = 'Lzb646767='
    ADMINS = ['thomaslzbuk@gamil.com']

    """
        the number of post records per page 
    """
    POSTS_PER_PAGE = 10

    LANGUAGES = ['en', 'zh']

    #ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    ELASTICSEARCH_URL = "http://127.0.0.1:9200"

    # use the Microsoft Translator API
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    #Redis URL
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
