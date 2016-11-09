from flask import (
    Blueprint,
    render_template,
)
from sqlalchemy.exc import SQLAlchemyError

from .models import Category

module = Blueprint('category', __name__)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/', methods=['GET'])
def index():
    categories = None
    try:
        categories = Category.query.filter(Category.parent_id.is_(None)).all()
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was uncaught database query', 'danger')
        abort(500)
    return render_template('category/index.html', categories=categories)