import os
import os.path as op

from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_babelex import Babel

from .warehouse.admin.views import CategoryView, TenantView, JumboImageView
from .warehouse.models import Category, Tenant, JumboImage
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'ru'

    admin = Admin(app, template_mode='bootstrap3')
    admin.add_view(TenantView(Tenant, db.session, name="Арендаторы"))
    admin.add_view(CategoryView(Category, db.session, name="Категории товаров"))
    admin.add_view(JumboImageView(JumboImage, db.session, name="Изображения (карусель)"))

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