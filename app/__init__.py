# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
from routes.Company import router as company_router


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../instance/config.py')

    app.register_blueprint(company_router, url_prefix="/api/companies")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
