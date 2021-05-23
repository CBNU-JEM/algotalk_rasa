# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from typing import Any, Text, Dict, List
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
        level = tracker.get_slot('level')
        example_code = tracker.get_slot('code')
        algorithm_name = tracker.get_slot('algorithm_type')

        algorithms = db.get_algorithm_by_name(algorithm_name)
        buttons = []
        explain_text = ""
        if algorithms and detail:
            explain_text = algorithms[0].detail_explain
            buttons = [{"title": "간단한 설명",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "brief":"간단한"}}"""},
                       {"title": "난이도",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "level":"난이도"}}"""},
                       {"title": "코드",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "code":"예제"}}"""},
                       {"title": "관련 문제", "payload": "/"}]
        elif algorithms:
            explain_text = algorithms[0].brief_explain
            buttons = [{"title": "자세한 설명",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "detail":"자세한"}}"""},
                       {"title": "난이도",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "level":"난이도"}}"""},
                       {"title": "코드",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "code":"예제"}}"""},
                       {"title": "관련 문제", "payload": "/"}]

        if algorithms and level:
            explain_text += f"\n난이도는 {algorithms[0].level}야"

        if algorithms and example_code:
            explain_text += f"\n예제 코드\n{algorithms[0].example_code}"

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        print(f"detail : {detail}")
        print(f"brief : {brief}")
        print(f"level : {level}")
        print(f"example_code : {example_code}")
        print(f"algorithm_name : {algorithm_name}")

        return [SlotSet("brief", None), SlotSet("detail", None), SlotSet("level", None), SlotSet("code", None)]


class ActionProblemRecommended(FormAction):

    def name(self) -> Text:
        return "action_problem_recommended"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        algorithm_name = tracker.get_slot('algorithm_type')
        number = tracker.get_slot('number')
        problem_name = tracker.get_slot('problem_name')
        contest_name = tracker.get_slot('contest_name')
        level = tracker.get_slot('level')
        if number is None :
            number = 1
        ##이름, 알고리즘, 난이도, 대회이름
        problem = db.get_problem(problem_name, algorithm_name, level, contest_name, number)

        buttons = []
        explain_text = ""
        #대회 문제면 대회버튼, 다른 문제 확인?
        if problem and contest_name:
            explain_text = problem[0].input
            explain_text += problem[0].output
            explain_text += problem[0].content
            buttons = [{"title": "사용 알고리즘",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}"}}"""},
                       {"title": "대회",
                        "payload": f"""/contest_type{{"contest_type": "{contest_name}"}}"""},
                       {"title": "난이도",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "level":"난이도"}}"""},
                       {"title": "다른 문제", "payload": "/"}]
        elif problem and number :
            explain_text = problem[0].input
            explain_text += problem[0].output
            explain_text += problem[0].content
            ## 알고리즘 db에서 검색 후 모두 출력
            buttons = [{"title": "사용 알고리즘",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}"}}"""},
                       {"title": "난이도",
                        "payload": f"""/algorithm_explain{{"algorithm_type": "{algorithm_name}", "level":"난이도"}}"""},
                       {"title": "다른 문제", "payload": "/"}]

        if problem and level:
            explain_text += f"\n난이도는 {problem[0].level}야"

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        print(f"number : {number}")
        print(f"problem_name : {problem_name}")
        print(f"level : {level}")
        print(f"contest_name : {contest_name}")
        print(f"algorithm_name : {algorithm_name}")

        return []


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
            "level": [self.from_entity(entity="level"), self.from_intent(intent="level", value=True)],
            "code": [self.from_entity(entity="code"), self.from_intent(intent="code", value=True)],
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


class ProblemForm(FormAction):

    def name(self) -> Text:
        return "problem_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["level"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "problem_name": [self.from_entity(entity="problem_name")],
            "contest_name": [self.from_entity(entity="contest_name"), self.from_intent(intent="contest_name")],
            "level": [self.from_entity(entity="level"), self.from_intent(intent="level", value=True)],
            "number": [self.from_entity(entity="number"), self.from_intent(intent="number")],
            "algorithm_type": [self.from_entity(entity="algorithm_type")]
        }
    def validate_level(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check algorithm_type"""
        # print(f"validate: ${tracker.get_latest_entity_values('brief_explain')}")
        print(f"level {value}")
        if (any(tracker.get_latest_entity_values('level'))):
            return {"level": value}
        else:
            return {"level": None}
    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        return []
