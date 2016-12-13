from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    g
)

from app.database import db

from sqlalchemy.exc import SQLAlchemyError

from flask import request
from flask_admin.form import thumbgen_filename

from werkzeug.useragents import UserAgent

from .models import Category, Tenant, JumboImage
from .forms import SearchForm
from ..utils.flask_utils import get_object_or_404

PAGE_SIZE = 9

module = Blueprint('warehouse', __name__)

allowed_static_pages = ['about', 'contacts', 'schema']
mobile_platforms = ["iphone", "android", "blackberry"]

@module.before_request
def before_request():
    g.search_form = SearchForm()
    g.categories = get_categories()
    g.is_mobile = is_mobile()

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/', methods=['GET'], defaults={'id': None})
@module.route('/categories/<int:id>', methods=['GET'])
@module.route('/categories/<int:id>/<int:page>', methods=['GET'])

def index(id, page=1):
    categories = get_categories()

    if id is not None:
        category = Category.query.get(id)
    else:
        category = categories[0]

    tenants_page = Tenant.query.filter(
                    Tenant.categories.contains(category)
                ).paginate(page, PAGE_SIZE)

    return render_template(
        'warehouse/index.html',
        jumbo_images=get_jumbo_images(),
        category=category,
        tenants_page=tenants_page,
        thumbgen_filename = thumbgen_filename
    )

@module.route('/tenants/<id>', methods=['GET'])
def show_tenant(id):
    
    tenant = get_object_or_404(Tenant, Tenant.id == id)
    return render_template(
        'warehouse/tenants.html',
        tenant=tenant
    )

@module.route('/search/', methods=['POST'])
def search():
    type(g.search_form.query)
    if not g.search_form.validate_on_submit():
        return redirect(url_for('warehouse.index'))
    return redirect(url_for('warehouse.search_results', query=g.search_form.query.data))

@module.route('/search_results/<query>')
def search_results(query):
    categories = Category.query.whoosh_search(query).all()
    tenants = Tenant.query.whoosh_search(query).all()

    return render_template(
        'warehouse/search_results.html',
        query=query,
        result={'categories': categories, 'tenants': tenants},
        thumbgen_filename = thumbgen_filename
    )

@module.route('/<string:page_name>/')
def static_page(page_name):
    if page_name in allowed_static_pages:
        return render_template(
            'warehouse/%s.html' % page_name
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

def get_jumbo_images():
    try:
        jumbo_images = JumboImage.query.all()
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was uncaught database query', 'danger')
        abort(500)
    return jumbo_images

def is_mobile():
    return UserAgent(request.user_agent.string).platform.lower() in mobile_platforms