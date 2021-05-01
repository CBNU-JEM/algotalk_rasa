# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
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
        # algorithm_name = tracker.latest_message['entities'][0]['value']
        brief = tracker.get_slot('brief')
        detail = tracker.get_slot('detail')
        algorithm_name = tracker.get_slot('algorithm_type')

        # print(tracker.get_latest_entity_values("정렬"))
        explain_text = "잘 모르곘어..."
        algorithms = db.get_algorithm_by_name(algorithm_name)
        buttons = []
        if algorithms and detail:
            explain_text = algorithms[0].detail_explain
            buttons = [{"title": "간단한 설명", "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "brief":"간단한"}}"""},
                       {"title": "난이도", "payload": "/"},
                       {"title": "코드", "payload": "/"},
                       {"title": "관련 문제", "payload": "/"}]
        elif algorithms:
            explain_text = algorithms[0].brief_explain
            buttons = [{"title": "자세한 설명", "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "detail":"자세한"}}"""},
                       {"title": "난이도", "payload": "/"},
                       {"title": "코드", "payload": "/"},
                       {"title": "관련 문제", "payload": "/"}]

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        print(f"detail : {detail}")
        print(f"brief : {brief}")
        print(f"algorithm_name : {algorithm_name}")

        return [SlotSet("brief", None), SlotSet("detail", None)]


class AlgorithmForm(FormAction):

    def name(self) -> Text:
        return "algorithm_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["algorithm_type"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "brief": [self.from_entity(entity="brief")],
            "detail": [self.from_entity(entity="detail")],
            "algorithm_type": [self.from_entity(entity="algorithm_type")]
        }

    # def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
    #     # type: () -> Dict[Text: Union[Text, Dict, List[Text, Dict]]]
    #     """algorithm_form"""
    #     return {"brief_explain": self.from_text(entity="algorithm_type")}
    #
    # def validate_brief(
    #         self,
    #         value: Text,
    #         dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     """check brief"""
    #     # print(f"validate: ${tracker.get_latest_entity_values('brief_explain')}")
    #     print(f"brief {value}")
    #     if (any(tracker.get_latest_entity_values('brief'))):
    #         return {"brief": True, "detail": None}
    #     else:
    #         return {"brief": None}
    #
    # def validate_detail(
    #         self,
    #         value: Text,
    #         dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     """check detail"""
    #     # print(f"validate: ${tracker.get_latest_entity_values('brief_explain')}")
    #     print(f"detail {value}")
    #     if (any(tracker.get_latest_entity_values('detail'))):
    #         return {"detail": True, "brief": None}
    #     else:
    #         return {"detail": None, "brief": True}

    def validate_algorithm_type(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check algorithm_type"""
        # print(f"validate: ${tracker.get_latest_entity_values('brief_explain')}")
        print(f"algorithm_type {value}")
        if (any(tracker.get_latest_entity_values('algorithm_type'))):
            return {"algorithm_type": value}
        else:
            return {"algorithm_type": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        return []
#     def validate_detail_explain(self, value, dispatcher, tracker, domain) -> Dict[Text, Any]:
#         """check detail"""
#         if(any(tracker.get_latest_entity_values("detail_explain"))):
#             return {"detail_explain": value}
#         else:
#             #dispatcher.utter_message(template="utter_what_algorithm")
#             return {"detail_explain": None}
