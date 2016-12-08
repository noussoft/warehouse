import os.path as op

from flask import url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView

from jinja2 import Markup
from wtforms.validators import InputRequired, Email, URL, Regexp, Length

from werkzeug import secure_filename

UPLOADS_DIR = op.join(op.join(op.join(op.dirname(__file__), '..'), '..'), 'static')

class CategoryView(ModelView):
    column_labels = dict(
        name='Название категории',
        main_category='Основная категория'
    )
    form_args = {
        'name': {
            'label': 'Название категории',
            'validators': [InputRequired("Введите название категории")]
        },
        'tenants': {
            'label': 'Арендаторы',
        },
        'categories': {
            'label': 'Подкатегории товаров',
        },
        'main_category': {
            'label': 'Основная категория',
        },
    }

class TenantView(ModelView):
    column_exclude_list = ['about']
    column_labels = dict(
        name='Арендатор',
        phone='Телефон',
        email='Эл. почта',
        www='Адрес сайта',
        place='Месторасположение',
        address='Адрес',
        about='Информация',
        image='Изображение',
        contact='Конт. лицо',
        keywords='Ключевые слова'
    )
    form_args = {
        'name': {
            'label': 'Арендатор',
            'validators': [InputRequired("Введите название арендатора")]
        },
        'phone': {
            'label': 'Телефон',
            'validators': [
                Length(min=10, max=10, message="Длина номера телефона 10 цифр, в формате XXXXXXXXXX"),
                InputRequired("Введите телефон"),
                Regexp(r'^\d{10}$', message="Телефон в формате XXXXXXXXXX")
            ]
        },
        'email': {
            'label': 'Email',
            'validators': [Email("Введите адрес электронной почты.")]
        },
        'www': {
            'label': 'Сайт',
            'validators': [URL(message="Введите адрес сайта арендатора.")]
        },
        'place': {
            'label': 'Месторасположение',
        },
        'address': {
            'label': 'Адрес',
        },
        'about': {
            'label': 'Информация',
        },
        'image': {
            'label': 'Изображение',
        },
        'contact': {
            'label': 'Контактное лицо',
        },
        'keywords': {
            'label': 'Ключевые слова',
        },
        'categories': {
            'label': 'Категории товара',
        },
    }

    def prefix_name(obj, file_data):
        parts = op.splitext(file_data.filename)
        return secure_filename('file_{}-{}{}'.format(obj.id, parts[0], parts[1]))

    form_extra_fields = {
        'image': form.ImageUploadField('Изображение',
                                    base_path=UPLOADS_DIR,
                                    thumbnail_size=(320, 150, True),
                                    namegen=prefix_name,
                                    relative_path='images/'
                                    ),
    }

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.image)))

    column_formatters = {
        'image': _list_thumbnail
    }

class JumboImageView(ModelView):
    column_labels = dict(
        image='Изображение'
    )
    form_args = {
        'image': {
            'label': 'Изображение',

        },
    }
    form_extra_fields = {
        'image': form.ImageUploadField('Изображение',
                                    base_path=UPLOADS_DIR,
                                    thumbnail_size=(800, 300, True),
                                    relative_path='jumbo_images/',
                                    validators=[InputRequired("Выберите файл с изображением")]
                                     ),
    }
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.image)))

    column_formatters = {
        'image': _list_thumbnail
    }