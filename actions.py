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

        print(tracker.latest_message)
        print(tracker.latest_message['entities'])
        explain_text = "잘 모르곘어..."
        if algorithm_type == "정렬":
            explain_text="정렬은 원소값을 오름차순이나 내림차순으로 수를 나열하는 알고리즘이야."
        elif algorithm_type == "최단거리":
            explain_text="최단거리 알고리즘은 네트워크에서 하나의 시작 정점으로부터 모든 다른 정점까지의 최단 경로를 찾는 알고리즘이야."
        elif algorithm_type == "스택":
            explain_text="스택은 마지막에 들어온 것이 먼저 나가는 LIFO(Last In First Out) 구조를 가진 자료 구조야"

        dispatcher.utter_message(explain_text)

        return []
