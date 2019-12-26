from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_uri = environ.get('DATABASE_URL', None)
db = SQLAlchemy()

def create_db(app, database_uri=database_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    db.create_all()
    migrate = Migrate(app, db)

import api.models.farmer