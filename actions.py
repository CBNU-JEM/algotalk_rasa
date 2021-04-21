# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionAlgorithmExplain(Action):

    def name(self) -> Text:
        return "action_algorithm_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        algorithm_type = tracker.latest_message['entities'][0]['value']

        explain_text = "잘 모르곘어..."
        if algorithm_type == "정렬":
            explain_text="정렬은 그게 아니야!"
        elif algorithm_type == "최단거리":
            explain_text="최단거리? 너무 어려운데"
        elif algorithm_type == "스택":
            explain_text="스택은 쉬운거야 찾아봐"

        dispatcher.utter_message(explain_text)

        return []
