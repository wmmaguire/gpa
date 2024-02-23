import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config(object):
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DATA_PATH = os.environ.get('DATA_PATH') or \
                    os.path.join(basedir, 'db/data')
    MAX_CONTENT_LENGTH = 1024 * 1024 #1MB
    UPLOAD_EXTENSIONS  = ['.jpg','.png', '.mp3', '.log']
    POSTS_PER_PAGE = 10
    ADMINS = ['wmm5035@gmail.com.com']
