from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uploads import configure_uploads, UploadSet
from flask_debugtoolbar import DebugToolbarExtension
from config import config, Config
import os
import time
from .utils.macros import format_date_thedaybefore, check_date, format_date, timestamp, product_has_sold
import mimetypes

mimetypes.add_type('image/svg+xml', '.svg')
toolbar = DebugToolbarExtension()
db = SQLAlchemy()
# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

# Flask-Uploads
PDF = ('pdf',)
uploaded_papers = UploadSet('papers', PDF)

# for reading files
APP_ROOT = os.path.dirname(os.path.abspath(
    __file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config[config_name])
    app.secret_key = config[config_name].SECRET_KEY

    db.init_app(app)
    configure_uploads(app, uploaded_papers)
    toolbar.init_app(app)

    # convert unicode to string
    app.jinja_env.filters['split'] = str.split
    app.jinja_env.filters['str'] = str
    app.jinja_env.filters['date_thedaybefore'] = format_date_thedaybefore
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.filters['unix_time'] = time.mktime
    app.jinja_env.filters['product_has_sold'] = product_has_sold

    from .modules.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
