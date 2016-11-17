from flask import (
    Blueprint,
    render_template,
)
from sqlalchemy.exc import SQLAlchemyError

from .models import Category

module = Blueprint('warehouse', __name__)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/categories/<id>', methods=['GET'])
@module.route('/', methods=['GET'], defaults={'id': None})
def index(id):
    categories = None
    try:
        categories = Category.query.filter(Category.parent_id.is_(None)).all()
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was uncaught database query', 'danger')
        abort(500)
    if id is not None:
        category = Category.query.get(id)
    else:
        category = categories[0]
    
    return render_template(
        'warehouse/index.html',
        categories=categories,
        category=category
    )