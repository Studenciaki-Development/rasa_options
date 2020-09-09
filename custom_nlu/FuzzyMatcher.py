from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.training_data import Message, TrainingData

from fuzzywuzzy import process, fuzz

import json
import os
import typing
from typing import Any, Optional, Text, Dict

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class FuzzyMatcher(Component):
    requires = ["tokens"]
    provides = ["entities"]
    defaults = {}
    supported_language_list = None
    threshold = 70

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)

    def train(
            self,
            training_data: TrainingData,
            config: Optional[RasaNLUModelConfig] = None,
            **kwargs: Any,
    ) -> None:
        pass

    @staticmethod
    def get_fuzzy_similarity(token=None, dictionary=None, min_ratio=None):
        """
        This function uses FuzzyWuzzy library to extract the most similar word from dictionary to token.text
        then if the similarity score is greater than min_ratio it returns it along with it's (entity key)
        """

        # Check for appropriate formats
        assert isinstance(token, str), "Tokens can be str() type only"
        assert isinstance(dictionary, dict), "Dictionary format should be provided in the dictionary parameter."
        assert isinstance(min_ratio, int), "Integer format should be provided in the minimum-ratio parameter."

        for key, values in dictionary.items():
            # search through the entire dictionary for the best match
            match = process.extractOne(token, values, scorer=fuzz.ratio)
            # Match is a tuple with the match value and the similary score.
            if min_ratio <= match[1]:
                return (match + (key,))

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message"""
        entities = list(message.get('entities'))
        # Get file path of lookup table in json format
        cur_path = os.path.dirname(__file__)
        if os.name == 'nt':
            partial_lookup_file_path = '..\\data\\lookup_table.json'
        else:
            partial_lookup_file_path = '../data/lookup_table.json'
        lookup_file_path = os.path.join(cur_path, partial_lookup_file_path)

        with open(lookup_file_path, 'r') as file:
            lookup_data = json.load(file)
            tokens = message.get('tokens')
            for token in tokens:
                similarity_score = self.get_fuzzy_similarity(token.text, lookup_data, self.threshold)
                if similarity_score is not None:
                    print("'" + token.text + "'" + " matches with " + str(similarity_score[0]) + "[" + similarity_score[
                        2] + "]" + " with a score of: " + str(similarity_score[1]))
                    for i, item in enumerate(entities):
                        # if entity already exist, update it (because diet classifier is higher in hierarchy)
                        if item['entity'] == similarity_score[2]:
                            item.update({"value": similarity_score[0]})
                    entities.append({
                        "start": token.start,
                        "end": token.end,
                        "value": similarity_score[0],
                        "confidence": similarity_score[1],
                        "entity": similarity_score[2]
                    })

        file.close()
        message.set("entities", entities, add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        pass

    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional["Metadata"] = None,
            cached_component: Optional["Component"] = None,
            **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            return cls(meta)
