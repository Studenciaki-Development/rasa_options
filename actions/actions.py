from actions.university.queries.queries import get_message, get_subject_limit
from .university.translate import translate_entity_name_to_subcategory, prepare_message
from .university.init_query import init_query
from .university.verify_limits import verify_limits

from typing import Any, Text, Dict, List

from rasa_sdk.events import AllSlotsReset
from rasa_sdk.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

FIELDS_OF_STUDY = [
    "fizyka",
    "informatyka",
    "matematyka",
    "chemia",
    "biologia",
    "automatyka",
    "zarządzanie",
]


class ActionGeneralOptions(Action):
    def name(self) -> Text:
        return "action_general_options"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        button_list = []
        selected_category = tracker.get_slot("category")
        subcategory = tracker.get_slot("subcategory")

        subcategory_list = init_query(selected_category, subcategory)

        for category in subcategory_list:
            title = f"{category.name}"
            payload = f"{category.payload}"
            button_list.append({"title": title, "payload": payload})

        if len(button_list) == 0:
            subcategory = translate_entity_name_to_subcategory(subcategory)
            message = get_message(subcategory)
            dispatcher.utter_message(text=message)
            print(f"{message}")
        else:
            message = "Wybierz kategorię pytania"
            dispatcher.utter_message(text=message, buttons=button_list)

        return [AllSlotsReset()]


class LimitForm(FormAction):
    def name(self) -> Text:
        return "form_get_field_of_study_limits"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        study_field = tracker.get_slot("field-of-study")

        if study_field not in FIELDS_OF_STUDY:
            return []

        limits = get_subject_limit(study_field)
        return verify_limits(limits)

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
            if isinstance(course_level, list):
                # sometimes rasa gets multiple slot values and saves them as a list
                # course-level: ['level1','level1']
                # we don't want that so I pick first value only
                course_level = course_level[0]
        except IOError:
            print(f"Error met while trying to get slots values in the LimitForm")
        if field_of_study in FIELDS_OF_STUDY:
            limit = get_subject_limit(field_of_study)
            msg = prepare_message(field_of_study, course_level, course_type, limit)
            dispatcher.utter_message(msg)
        else:
            dispatcher.utter_message("Nie zrozumiałem twojego zapytania, albo na naszej uczelni nie ma takiego "
                                     "kierunku.")

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
