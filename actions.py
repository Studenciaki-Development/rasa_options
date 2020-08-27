from university.queries.queries import get_message, get_subject_limit
from university.translate import translate_entity_name_to_subcategory, prepare_message
from university.init_query import init_query

from typing import Any, Text, Dict, List

from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
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


class LimitForm(FormAction):
    def name(self) -> Text:
        return "form_limits"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        study_field = tracker.get_slot("field-of-study")

        if study_field not in FIELDS_OF_STUDY:
            return []

        limits = get_subject_limit(study_field)

        if limits["limit_niestat1"] is None and limits["limit_niestat2"] is None:
            return ["field-of-study", "course-level"]
        elif limits["limit_stat2"] is None and limits["limit_niestat2"] is None:
            return ["field-of-study", "course-type"]
        elif limits["limit_stat1"] is None and limits["limit_stat2"] is None:
            return ["field-of-study", "course-level"]
        else:
            return ["field-of-study", "course-level", "course-type"]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        try:
            field_of_study = tracker.get_slot("field-of-study")
            course_level = tracker.get_slot("course-level")
            course_type = tracker.get_slot("course-type")
        except:
            pass

        limit = get_subject_limit(field_of_study)

        msg = prepare_message(field_of_study, course_level, course_type, limit)

        dispatcher.utter_message(msg)

        return [AllSlotsReset()]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {
            "field-of-study": self.from_entity(
                entity="field-of-study", intent=["get_field_of_study"]
            ),
            "course_level": self.from_entity(
                entity="course-level", intent=["get_course_level"]
            ),
            "course-type": self.from_entity(
                entity="course-type", intent=["get_course_type"]
            ),
        }
