# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from actions import db


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionAlgorithmExplain(FormAction):

    def name(self) -> Text:
        return "action_algorithm_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #algorithm_name = tracker.latest_message['entities'][0]['value']
        algorithm_name = tracker.get_latest_entity_values("algorithm_type")
        print(algorithm_name)
        print(tracker.get_latest_entity_values("정렬"))
        explain_text = "잘 모르곘어..."
        algorithms = db.get_algorithm_by_name(algorithm_name)
        if algorithms:
            explain_text = algorithms[0].brief_explain

        dispatcher.utter_message(explain_text)

        return []


class AlgorithmForm(FormAction):

    def name(self) -> Text:
        return "algorithm_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["algorithm_type"]

    def slot_mapping(self):
        # type: () -> Dict[Text: Union[Text, Dict, List[Text, Dict]]]
        """algorithm_form"""

        return {"brief_explain": self.from_entity(entity="algorithm_type", intent="base_explain"),
                "detail_explain": self.from_entity(entity="algorithm_type", intent="detail_explain"),
                }

    def validate_brief_explain(self, value, dispatcher, tracker, domain) -> Dict[Text, Any]:
        """check brief"""
        if(any(tracker.get_latest_entity_values("brief_explain"))):
            return {"brief_explain": value}
        else:
            #dispatcher.utter_message(template="utter_what_algorithm")
            return {"brief_explain": None}

    def submit(self,
    			   dispatcher: CollectingDispatcher,
    			   tracker: Tracker,
    			   domain: Dict[Text, Any]) -> List[Dict]:
    		"""Define what the form has to do
    			after all required slots are filled"""

    		# utter submit template

    		return []
#     def validate_detail_explain(self, value, dispatcher, tracker, domain) -> Dict[Text, Any]:
#         """check detail"""
#         if(any(tracker.get_latest_entity_values("detail_explain"))):
#             return {"detail_explain": value}
#         else:
#             #dispatcher.utter_message(template="utter_what_algorithm")
#             return {"detail_explain": None}