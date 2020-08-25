from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

Base = declarative_base()
engine = create_engine("sqlite:///db/uczelnia.db")

class Categories(Base):
    __table__ = Table('categories', Base.metadata, autoload=True, autoload_with=engine)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine) 

def getInfo(category):
    print(f"1 category {category}")
    session = Session()
    try:
        message = session.query(Categories.message).filter(Categories.name==category).one()
        session.close()
        return message[0]
    except:
        message = "Error"
        return message

def getCategories(category):
    session = Session()
    try:
        category_id = session.query(Categories.id).filter(Categories.name==category)
        subcategoryList = session.query(Categories).filter(
            Categories.parent_id == category_id)
        session.close()

        return subcategoryList
    except:
        return [0, 0]

def translateEntity(subcategory):
    if subcategory == '1turn':
        subcategory = "Rozpoczęcie rekrutacji"
    elif subcategory== "2turn":
        subcategory = "Druga tura"
    elif subcategory== "limits":
        subcategory = "Limity przyjęć"
    elif subcategory== "courses":
        subcategory = "Lista kierunków"
    elif subcategory== "available":
        subcategory = "Wolne miejsca"
    elif subcategory== "recruitment_costs":
        subcategory = "Opłata rekrutacyjna"
    elif subcategory== "students_costs":
        subcategory = "Opłata za studia"
    elif subcategory== "returns":
        subcategory = "Zwrot opłat"
    return subcategory

def parseQuery(selected_category,subcategory):
        if subcategory is not None:
            subcategory = translateEntity(subcategory)
            subcategoryList = getCategories(subcategory)
        elif selected_category is not None:
            subcategoryList = getCategories(selected_category)
        else:
            subcategoryList = getCategories('root') 

        return subcategoryList

class ActionGeneralOptions(Action):

    def name(self) -> Text:
        return "action_general_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttonList = []
        selected_category = tracker.get_slot("category")
        subcategory = tracker.get_slot("subcategory")

        subcategoryList = parseQuery(selected_category,subcategory)

        for category in subcategoryList:
            title = f"{category.name}"
            payload = f"{category.payload}"
            buttonList.append({"title": title, "payload": payload})

        if(len(buttonList) == 0):
            subcategory=translateEntity(subcategory)
            print(f"1 subcategory {subcategory}")
            message = getInfo(subcategory)
            dispatcher.utter_message(text=message)
        else:
            message = "Wybierz kategorię pytania"
            dispatcher.utter_message(text=message, buttons=buttonList)


        return [AllSlotsReset()]
