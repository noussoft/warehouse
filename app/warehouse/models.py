from app.database import db

categories_tenants_table = db.Table('categories_tenants',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
    db.Column('tenant_id', db.Integer, db.ForeignKey('tenants.id'))
)

class Category(db.Model):
    __tablename__ = 'categories'
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(255), index = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    categories = db.relationship(
        "Category",
        backref = db.backref('main_category', remote_side=id),
        lazy="dynamic"
    )

    tenants = db.relationship("Tenant",
        secondary=categories_tenants_table,
        backref=db.backref("categories", lazy='dynamic'))


    def __str__(self):
        return self.name

class Tenant(db.Model):
    __tablename__ = 'tenants'
    __searchable__ = ['name', 'about', 'keywords']

    id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(255), index = True)
    phone = db.Column(db.String(11), index = False)
    # {64}@{255} RFC 3696
    email = db.Column(db.String(320), index = False)
    www = db.Column(db.String(255), index = False)
    place = db.Column(db.String(255), index = False)
    address = db.Column(db.String(255), index = False)
    about = db.Column(db.Text, index = False)
    image = db.Column(db.String(255), index = False)
    contact = db.Column(db.String(255), index = False)
    keywords = db.Column(db.String(255), index = True)

    def __str__(self):
        return self.name

class JumboImage(db.Model):
    __tablename__ = 'jumbo_image'

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(255), index = False)