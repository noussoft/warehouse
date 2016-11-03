from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    name =  Column(String(255), index = True)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    categories = relationship(
        "Category",
        backref = backref('main_category', remote_side=id),
        lazy="dynamic"
    )