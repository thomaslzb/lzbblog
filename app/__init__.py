import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from elasticsearch import Elasticsearch #Full-Text Search Engine

from flask import Flask,current_app
from flask import request
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config

from redis import Redis
import rq


db = SQLAlchemy()

migrate = Migrate(db)

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


@babel.localeselector
def get_locale():
    my_lang = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # my_lang = 'en'
    return my_lang


def create_app(config_class = Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)

    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    if app.config['ELASTICSEARCH_URL'] :
       app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']], verify_certs=True)
    else:
        app.elasticsearch =None

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('lzbblog-tasks', connection=app.redis)

    # register blueprint
    from app.error import bp as error_bp
    app.register_blueprint(error_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    if not app.debug or not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Myblog Failure Message',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        """
        # Email Configuration
            logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

            logging.debug('This is debug message')
            logging.info('This is info message')
            logging.warning('This is warning message')
            logging.basicConfig函数各参数:
                filename: 指定日志文件名
                filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
                format: 指定输出的格式和内容，format可以输出很多有用信息，如上例所示:
                     %(levelno)s: 打印日志级别的数值
                     %(levelname)s: 打印日志级别名称
                     %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
                     %(filename)s: 打印当前执行程序名
                     %(funcName)s: 打印日志的当前函数
                     %(lineno)d: 打印日志的当前行号
                     %(asctime)s: 打印日志的时间
                     %(thread)d: 打印线程ID
                     %(threadName)s: 打印线程名称
                     %(process)d: 打印进程ID
                     %(message)s: 打印日志信息
                    datefmt: 指定时间格式，同time.strftime()
                    level: 设置日志级别，默认为logging.WARNING
                    stream: 指定将日志的输出流，可以指定输出到sys.stderr,sys.stdout或者文件，
                    默认输出到sys.stderr，当stream和filename同时指定时，stream被忽略
        """
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/Myblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Myblog startup')

    return app
