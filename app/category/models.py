from app.database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(255), index = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    categories = db.relationship(
        "Category",
        backref = db.backref('main_category', remote_side=id),
        lazy="dynamic"
    )

    def __str__(self):
        return self.name