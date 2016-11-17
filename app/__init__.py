import os
from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from .warehouse.models import Category, Tenant
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    admin = Admin(app, template_mode='bootstrap3')
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Tenant, db.session))

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

    import app.warehouse.controllers as warehouse
    import app.general.controllers as general

    app.register_blueprint(warehouse.module)
    app.register_blueprint(general.module)

    return app