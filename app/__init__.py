import os
from flask import Flask
from flask_migrate import Migrate
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.test_request_context():
        db.create_all()

    if app.debug == True:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            toolbar = DebugToolbarExtension(app)
        except:
            pass

    import app.category.controllers as category
    import app.general.controllers as general

    app.register_blueprint(category.module)
    app.register_blueprint(general.module)

    return app