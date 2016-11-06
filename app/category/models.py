from app.database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(db.Integer, primary_key = True)
    name =  Column(db.String(255), index = True)
    parent_id = Column(db.Integer, db.ForeignKey('categories.id'))

    categories = db.relationship(
        "Category",
        backref = backref('main_category', remote_side=id),
        lazy="dynamic"
    )

    def __str__(self):
        return self.name