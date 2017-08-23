import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'somesecretkey'

    LAZYLOAD_LDA = False
    ALLOW_ANON = True
    DEFAULT_LDA_MODEL = 'Demo'
    DEFAULT_DB = 'Demo Keyword-based Model'
    # Flask-Uploads configs - used in /app/__init__.py
    # the names has the format: UPLOADED_[]_DEST defined by Flask-Uploads
    UPLOADED_PAPERS_DEST = os.environ.get(
        'UPLOADED_PAPERS_DEST') or basedir + '/app/static/upload/papers/'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    # debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

anon = {
    "family_name": "",
    "user_id": "0",
    "name": "Anonymous",
    "picture": "https://randomuser.me/api/portraits/lego/1.jpg",
    "locale": "en",
    "email_verified": True,
    "nickname": "Anon",
    "given_name": "",
    "email": "anon@example.com",
}
