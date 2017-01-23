import os
import os.path as op
import flask_whooshalchemy as whooshalchemy

from flask import Flask, url_for
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_migrate import Migrate
from flask_babelex import Babel

from flask.ext.security import Security, SQLAlchemyUserDatastore

from .warehouse.admin.views import CategoryView, TenantView, JumboImageView
from .warehouse.models import Category, Tenant, JumboImage, Role, User
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'ru'

    admin = Admin(
        app,
        'База на Врубовой',
        base_template='my_master.html',
        template_mode='bootstrap3',
    )
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

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
    )

    import app.warehouse.controllers as warehouse
    import app.general.controllers as general

    app.register_blueprint(warehouse.module)
    app.register_blueprint(general.module)

    whooshalchemy.whoosh_index(app, Category)
    whooshalchemy.whoosh_index(app, Tenant)

    return app