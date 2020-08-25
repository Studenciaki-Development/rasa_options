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

class ActionGeneralOptions(Action):

    def name(self) -> Text:
        return "action_general_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttonList = []
        selected_category = tracker.get_slot("category")
        print(f"1 Selected category {selected_category}")

        if selected_category is None:
            categories = getCategories('root') 
        else:
            if selected_category == 'deadlines':
                selected_category='Terminy'
            elif selected_category == 'costs':
                selected_category='Opłaty'
            elif selected_category == 'recruitment':
                selected_category='Rekrutacja'
            categories = getCategories(selected_category)

        for category in categories:
            title = f"{category.name}"
            payload = f"{category.payload}"
            buttonList.append({"title": title, "payload": payload})

        message = "Test message 1"
        dispatcher.utter_message(text=message, buttons=buttonList)

        return [AllSlotsReset()]
