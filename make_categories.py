import re
import urllib.request

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import create_database

from bs4 import BeautifulSoup

from settings import DB_USER, DB_PASSWORD, DB_NAME
from settings import URL_TO_PARSE

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

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_categories(html):
    soup = BeautifulSoup(html, "html.parser")
    categories_list = soup.find('ul', class_="children-list")
    items = categories_list.find_all('li')
    
    categories = dict()
    for i, item in enumerate(items):

        matches = re.match(
            r'(\d{1,2})\.(\d{1,2})?\.?(\d{1,2})?\.?(.*)',
            item.get_text().strip()
        )
        
        if (matches and matches.groups()[0] == '2'):

            if (matches.groups()[2] == None):
                categories[matches.groups()[3].strip()] = []
                parent_id = matches.groups()[1]
                parent_name = matches.groups()[3].strip()
            elif (matches.groups()[1] == parent_id):
                categories[parent_name].append(matches.groups()[3].strip())
    
    return categories


def main():
    engine = create_engine(
        'mysql://{}:{}@localhost/{}?charset=utf8'.format(
            DB_USER, DB_PASSWORD, DB_NAME
        )
    )

    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)

    Session = sessionmaker(bind = engine)
    session = Session()
    
    categories = get_categories(get_html(URL_TO_PARSE))

    for name in categories:
        category = Category(name = name)
        session.add(category)
        session.flush()
        for subname in categories[name]:
            session.add(Category(name = subname, parent_id = category.id))
    
    session.commit()

if __name__ == '__main__':
    main()