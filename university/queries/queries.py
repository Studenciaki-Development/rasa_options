from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///db/uczelnia.db")


class Categories(Base):
    __table__ = Table("categories", Base.metadata, autoload=True, autoload_with=engine)


class ListOfStudyFields(Base):
    __table__ = Table("przedmioty", Base.metadata, autoload=True, autoload_with=engine)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_message(category):
    session = Session()
    try:
        message = (
            session.query(Categories.message).filter(Categories.name == category).one()
        )
        session.close()
        return message[0]
    except:
        message = "Ups. Coś poszło nie tak"
        return message


def get_categories(category):
    session = Session()
    try:
        category_id = session.query(Categories.id).filter(Categories.name == category)
        subcategoryList = session.query(Categories).filter(
            Categories.parent_id == category_id
        )
        session.close()

        return subcategoryList
    except:
        return [0, 0]


def get_subject_limit(study_field):
    session = Session()

    try:
        question_target = (
            session.query(ListOfStudyFields)
            .filter(ListOfStudyFields.nazwa == study_field)
            .one()
        )
    except:
        return []

    limit_stat1 = question_target.stacjonarne_s1
    limit_stat2 = question_target.stacjonarne_s2
    limit_niestat1 = question_target.niestacjonarne_s1
    limit_niestat2 = question_target.niestacjonarne_s2
    session.close()
    return {
        "limit_stat1": limit_stat1,
        "limit_stat2": limit_stat2,
        "limit_niestat1": limit_niestat1,
        "limit_niestat2": limit_niestat2,
    }
