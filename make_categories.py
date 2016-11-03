import urllib.request

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import create_database

from bs4 import BeautifulSoup

from settings import DB_USER, DB_PASSWORD, DB_NAME

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    name =  Column(String(50), index = True)


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def main():
    engine = create_engine(
        'mysql://{}:{}@localhost/{}'.format(DB_USER, DB_PASSWORD, DB_NAME)
    )
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
