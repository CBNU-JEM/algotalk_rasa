# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.forms import FormAction
from rasa_sdk.events import (SlotSet, UserUtteranceReverted, ConversationPaused, EventType, ActionExecuted, UserUttered)
from rasa_sdk import Action, Tracker
from typing import Any, Dict, List, Text, Union, Optional
from rasa_sdk.executor import CollectingDispatcher
import logging

logger = logging.getLogger(__name__)

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
            explain_text="정렬은 원소값을 오름차순이나 내림차순으로 수를 나열하는 알고리즘이야."
        elif algorithm_type == "최단거리":
            explain_text="최단거리 알고리즘은 네트워크에서 하나의 시작 정점으로부터 모든 다른 정점까지의 최단 경로를 찾는 알고리즘이야."
        elif algorithm_type == "스택":
            explain_text="스택은 스택은 마지막에 들어온 것이 먼저 나가는 LIFO(Last In First Out) 구조를 가진 자료 구조야"

        dispatcher.utter_message(explain_text)

        return []

# class ProblemForm(FormAction):
#
#     def name(self) -> Text:
#         return "problem_form"
#
#     def required_slots(tracker: "Tracker") -> List[Text]:
#         return["problem_name", "problem_level", "problem_content", "problem_input", "problem_output", "problem_source", "problem_uri"]
#
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
#         return {
#             "problem_name": [self.from_entity(entity="problem_name"),
#                                 self.from_text(intent="problem_info")],
#             "problem_level": self.from_entity(entity="problem_level"),
#             "problem_content": [self.from_entity(entity="problem_content"),
#                                     self.from_text(intent="problem_info")],
#             "problem_input": [self.from_entity(entity="problem_input"),
#                                 self.from_text(intent="problem_info")],
#             "problem_output": [self.from_entity(entity="problem_output"),
#                                 self.from_text(intent="problem_info")],
#             "problem_source": [self.from_entity(entity="problem_source"),
#                                 self.from_text(intent="problem_info")],
#             "problem_uri": self.from_entity(entity="problem_uri")
#         }
#
#     def submit(
#         self,
#         dispatcher: "CollectingDispatcher",
#         tracker: "Tracker",
#         domain: "DomainDict",
#     ) -> List[EventType]:
#         dispatcher.utter_message("모야모야")
#         return []

# {
#     'intent':
#         {
#             'name': 'algorithm_explain',
#             'confidence': 0.977513313293457
#          },
#     'entities':
#         [
#             {
#                 'start': 0,
#                 'end': 2,
#                 'value': '정렬',
#                 'entity': 'algorithm_type',
#                 'confidence': 0.9636158016518531,
#                 'extractor': 'CRFEntityExtractorKorean'
#             },
#             {
#                 'entity': 'algorithm_type',
#                 'start': 0,
#                 'end': 2,
#                 'extractor': 'DIETClassifier',
#                 'value': '정렬'
#             }
#         ],
#     'intent_ranking':
#         [
#             {
#                 'name': 'algorithm_explain',
#                 'confidence': 0.977513313293457
#             },
#             {
#                 'name': 'recommendation_type',
#                 'confidence': 0.006358877755701001
#             },
#             {
#                 'name': 'detail_explain',
#                 'confidence': 0.0049648680724200004
#             },
#             {
#                 'name': 'contest_detail_information',
#                 'confidence': 0.004869600292295001
#             },
#             {
#                 'name': 'goodbye',
#                 'confidence': 0.003942569717764
#             },
#             {
#                 'name': 'base_explain',
#                 'confidence': 0.000575865269638
#             },
#             {
#                 'name': 'problem_site',
#                 'confidence': 0.0005688776145680001
#             },
#             {
#                 'name': 'recommendation_level',
#                 'confidence': 0.00044134684139800006
#             },
#             {
#                 'name': 'problem_type',
#                 'confidence': 0.000385548191843
#             },
#             {
#                 'name': 'deny',
#                 'confidence': 0.00037916220026000004
#             }
#         ],
#     'text': '정렬 알고리즘'
# }