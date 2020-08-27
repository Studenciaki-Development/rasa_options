from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///db/uczelnia.db")

class Categories(Base):
    __table__ = Table('categories', Base.metadata, autoload=True, autoload_with=engine)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine) 

def get_message(category):
    session = Session()
    try:
        message = session.query(Categories.message).filter(Categories.name==category).one()
        session.close()
        return message[0]
    except:
        message = "Ups. Coś poszło nie tak"
        return message

def get_categories(category):
    session = Session()
    try:
        category_id = session.query(Categories.id).filter(Categories.name==category)
        subcategoryList = session.query(Categories).filter(
            Categories.parent_id == category_id)
        session.close()

        return subcategoryList
    except:
        return [0, 0]
