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

def getCategories(category):
    session = Session()

    try:
        category_id = session.query(Categories.id).filter(Categories.name==category)

        categories = session.query(Categories).filter(
            Categories.parent_id == category_id)
        
        return categories
    except:
        return []

def parseQuery(selected_category,subcategory_deadlines):
        if subcategory_deadlines is not None:
            if subcategory_deadlines == '1turn':
                subcategory_deadlines = "Rozpoczęcie rekrutacji"
            elif subcategory_deadlines== "2turn":
                subcategory_deadlines = "Druga tura"
            categories = getCategories(subcategory_deadlines)
        elif selected_category is not None:
            categories = getCategories(selected_category)
        else:
            categories = getCategories('root') 


        return categories

class ActionGeneralOptions(Action):

    def name(self) -> Text:
        return "action_general_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttonList = []
        selected_category = tracker.get_slot("category")
        subcategory_deadlines = tracker.get_slot("subcategory_Terminy")

        print(f"1 Selected category {selected_category}")
        print(f"1 Selected category {subcategory_deadlines}")
        categories = parseQuery(selected_category,subcategory_deadlines)

        for category in categories:
            title = f"{category.name}"
            payload = f"{category.payload}"
            buttonList.append({"title": title, "payload": payload})


        message = "Test message 1"
        dispatcher.utter_message(text=message, buttons=buttonList)

        return [AllSlotsReset()]
