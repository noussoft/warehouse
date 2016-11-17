from flask_admin.contrib.sqla import ModelView
from wtforms.validators import InputRequired, Email, URL, Regexp

class CategoryView(ModelView):
    column_labels = dict(
        name='Название категории', main_category='Основная категория'
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
    )
    form_args = {
        'name': {
            'label': 'Арендатор',
            'validators': [InputRequired("Введите название арендатора")]
        },
        'phone': {
            'label': 'Телефон',
            'validators': [
                InputRequired("Введите телефон"),
                Regexp('\d{10}', message="Телефон в формате XXXXXXXXXX")
            ]
        },
        'email': {
            'label': 'Email',
            'validators': [Email("Введите адрес электронной почты.")]
        },
        'www': {
            'label': 'WWW',
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
        'categories': {
            'label': 'Категории товара',
        },
    }