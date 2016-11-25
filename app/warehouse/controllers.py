from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
)

from app.database import db

from sqlalchemy.exc import SQLAlchemyError

from .models import Category, Tenant
from ..utils.flask_utils import get_object_or_404

module = Blueprint('warehouse', __name__)

allowed_static_pages = ['about', 'contacts', 'schema']

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/categories/<id>', methods=['GET'])
@module.route('/', methods=['GET'], defaults={'id': None})
def index(id):
    categories = get_categories()

    if id is not None:
        category = Category.query.get(id)
    else:
        category = categories[0]
    
    return render_template(
        'warehouse/index.html',
        categories=categories,
        category=category
    )

@module.route('/tenants/<id>', methods=['GET'])
def show_tenant(id):
    
    tenant = get_object_or_404(Tenant, Tenant.id == id)
    return render_template(
        'warehouse/tenants.html',
        tenant=tenant,
        categories=get_categories()
    )

@module.route('/<string:page_name>/')
def static_page(page_name):
    if page_name in allowed_static_pages:
        return render_template(
            'warehouse/%s.html' % page_name,
            categories=get_categories()
        )
    return redirect(url_for('warehouse.index'))

def get_categories():
    try:
        categories = Category.query.filter(
            db.and_(
                Category.parent_id.is_(None),
                Category.tenants.any()
            )
        ).all()
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was uncaught database query', 'danger')
        abort(500)
    return categories