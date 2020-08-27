from university.queries.queries import get_message
from university.translate import translate_entity_name_to_subcategory
from university.initQuery import init_query
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGeneralOptions(Action):
    def name(self) -> Text:
        return "action_general_options"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        buttonList = []
        selected_category = tracker.get_slot("category")
        subcategory = tracker.get_slot("subcategory")

        subcategoryList = init_query(selected_category, subcategory)

        for category in subcategoryList:
            title = f"{category.name}"
            payload = f"{category.payload}"
            buttonList.append({"title": title, "payload": payload})

        if len(buttonList) == 0:
            subcategory = translate_entity_name_to_subcategory(subcategory)
            message = get_message(subcategory)
            dispatcher.utter_message(text=message)
            print(f"{message}")
        else:
            message = "Wybierz kategorię pytania"
            dispatcher.utter_message(text=message, buttons=buttonList)

        return [AllSlotsReset()]
