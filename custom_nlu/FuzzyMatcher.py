from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.training_data import Message, TrainingData

from fuzzywuzzy import process

import json
import os
import typing
from typing import Any, Optional, Text, Dict, List, Type

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class FuzzyMatcher(Component):
    provides = ["entities"]
    requires = ["tokens"]
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
            lookup_data = json.load(file)['data']

            tokens = message.get('tokens')
            print(lookup_data)
            for token in tokens:
                fuzzy_results = process.extract(
                    token.text,
                    lookup_data,
                    limit=5)
                print(fuzzy_results)
                for result, confidence in fuzzy_results:
                    if confidence >= self.threshold:
                        print("value", result["value"])
                        print('entity', result["entity"])
                        entities.append({
                            "start": token.start,
                            "end": token.end,
                            "value": token.text,
                            "fuzzy_value": result["value"],
                            "confidence": confidence,
                            "entity": result["entity"]
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
