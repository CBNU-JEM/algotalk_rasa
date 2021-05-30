# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from actions import db
from actions.func import level_up, level_down


class ActionLevelChangeEasy(Action):
    def name(self) -> Text:
        return "action_level_change_easy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        level = tracker.get_slot('level')
        print(f"\nlevel= {level}")
        level_up(level)
        return [SlotSet('level', level)]


class ActionLevelChangeHard(Action):
    def name(self) -> Text:
        return "action_level_change_hard"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        level = tracker.get_slot('level')
        print(f"\nlevel= {level}")
        level_down(level)
        return [SlotSet('level', level)]


class ActionAlgorithmExplain(FormAction):
    def name(self) -> Text:
        return "action_algorithm_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        brief = tracker.get_slot('brief')
        detail = tracker.get_slot('detail')
        level = tracker.get_slot('level')
        example_code = tracker.get_slot('code')
        algorithm_name = tracker.get_slot('algorithm_name')

        algorithms = db.get_algorithm_by_name(algorithm_name)
        buttons = []
        explain_text = ""
        if algorithms and detail:
            if algorithms[0].detail_explain:
                explain_text = algorithms[0].detail_explain
                buttons = [{"title": "간단한 설명",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "brief":"간단한"}}"""},
                           {"title": "난이도",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "level":"난이도"}}"""},
                           {"title": "코드",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "code":"예제"}}"""},
                           {"title": "문제 추천",
                            "payload": f"""/problem_type{{"level":"{level}, "algorithm_name:"{algorithm_name}"}}"""}]
            elif algorithms[0].brief_explain:
                explain_text = f"자세하게는 나도 모르겠어. 대신 간단하게 설명해줄게.\n{algorithms[0].brief_explain}"
                buttons = [{"title": "난이도",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "level":"난이도"}}"""},
                           {"title": "코드",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "code":"예제"}}"""},
                           {"title": "문제 추천",
                            "payload": f"""/problem_type{{"level":"{level}, "algorithm_name:"{algorithm_name}"}}"""}]
            else:
                explain_text = f"나도 잘 모르겠어.";
        elif algorithms:
            if algorithms[0].brief_explain:
                explain_text = algorithms[0].brief_explain
                buttons = [{"title": "자세한 설명",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "detail":"자세한"}}"""},
                           {"title": "난이도",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "level":"난이도"}}"""},
                           {"title": "코드",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "code":"예제"}}"""},
                           {"title": "문제 추천",
                            "payload": f"""/problem_type{{"level":"{level}, "algorithm_name":"{algorithm_name}"}}"""}]
            else:
                explain_text = f"나도 잘 모르겠어.";

        if algorithms and level and algorithms[0].level:
            if algorithms[0].example_code:
                explain_text += f"\n난이도는 {algorithms[0].level}야"
            else:
                explain_text += f"\n난이도는 모르겠어."

        if algorithms and example_code:
            if algorithms[0].example_code:
                explain_text += f"\n예제 코드\n{algorithms[0].example_code}"
            else:
                explain_text += f"\n예제 코드는 준비중이야."

        if algorithms is None:
            explain_text = "그런 알고리즘은 처음 들어봐."

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        print(algorithms)
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
        algorithm_name = tracker.get_slot('algorithm_name')
        number = tracker.get_slot('number')
        problem_name = tracker.get_slot('problem_name')
        contest_name = tracker.get_slot('contest_name')
        level = tracker.get_slot('level')
        if number is None:
            number = 1
        ##이름, 알고리즘, 난이도, 대회이름
        problem = db.get_problem(problem_name, algorithm_name, level, contest_name, number)
        print(problem)
        buttons = []
        explain_text = ""
        if problem and contest_name:
            if problem[0].name:
                explain_text += "이름\n" + problem[0].name
            else:
                explain_text += "이름 : 없음"
            if problem[0].input:
                explain_text += "\n입력\n" + problem[0].input
            else:
                explain_text += "\n입력 : 없음"
            if problem[0].output:
                explain_text += "\n출력\n" + problem[0].output
            else:
                explain_text += "\n출력 : 없음"
            if problem[0].content:
                explain_text += "\n설명\n" + problem[0].content
            else:
                explain_text += "\n설명 : 없음"

            buttons = [{"title": "사용 알고리즘",
                        "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}"""},
                       {"title": "대회",
                        "payload": f"""/contest_explain{{"contest_name": "{contest_name}"}}"""},
                       # {"title": "난이도",
                       #  "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "level":"{난이도}"}}"""},
                       {"title": "다른 문제",
                        "payload": f"""/problem_type{{"algorithm_name":"{algorithm_name}"}}"""}]
        elif problem and number:
            if problem[0].name:
                explain_text += "이름\n : " + problem[0].name
            else:
                explain_text += "이름 : 없음"
            if problem[0].input:
                explain_text += "\n입력\n : " + problem[0].input
            else:
                explain_text += "\n입력 : 없음"
            if problem[0].output:
                explain_text += "\n출력\n : " + problem[0].output
            else:
                explain_text += "\n출력 : 없음"
            if problem[0].content:
                explain_text += "\n설명\n" + problem[0].content
            else:
                explain_text += "\n설명 : 없음"
            # 알고리즘 db에서 검색 후 모두 출력
            buttons = [{"title": "사용 알고리즘",
                        "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}"""},
                       # {"title": "난이도",
                       #  "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "level":"난이도"}}"""},
                       {"title": "다른 문제",
                        "payload": f"""/problem_type{{"algorithm_name":"{algorithm_name}"}}"""}]

        if problem and level:
            if problem[0].level:
                explain_text += f"\n난이도는 {problem[0].level}야"
            else:
                explain_text += f"\n난이도 : 없음"

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

        return ["algorithm_name"]

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
            "algorithm_name": [self.from_entity(entity="algorithm_name")]
        }

    def validate_algorithm_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check algorithm_name"""

        print(f"algorithm_name {value}")
        return {"algorithm_name": value}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        return []


class ActionContestExplain(FormAction):

    def name(self) -> Text:
        return "action_contest_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        brief = tracker.get_slot('brief')
        detail = tracker.get_slot('detail')
        past = tracker.get_slot('past')
        proceeding = tracker.get_slot('proceeding')
        reception_period = tracker.get_slot('reception_period')

        schedule = tracker.get_slot('schedule')
        contest_name = tracker.get_slot('contest_name')

        contests = db.get_contest_by_name(contest_name)
        # contest를 시간순으로 정렬하고 필터링해서 출력한다.
        contests.sort(key=lambda x: x.contest_start)
        today = datetime.datetime.now()
        if past:
            contests = list(filter(lambda x: x.date < today, contests))
        elif proceeding:
            contests = list(filter(lambda x: x.reception_start <= today <= x.reception_end, contests))

        buttons = []
        explain_text = ""
        if contests:
            explain_text = contests[0].content
            buttons = [{"title": "대회 일정",
                        "payload": f"""/contest_explain{{"contest_name": "{contest_name}", "schedule":"일정"}}"""},
                       {"title": "대회 홈페이지",
                        "payload": f"""/contest_explain{{"contest_name": "{contest_name}", "homepage":"홈페이지"}}"""},
                       {"title": "신청 기간", "payload": f"""/contest_explain{{"contest_name": "{contest_name}", "reception_period":"신청 기간"}}"""}]

        if reception_period:
            if contests[0].reception_start and contests[0].reception_end:
                explain_text += "\n신청 기간은 " + contests[0].reception_start + "부터 " + contests[0].reception_end + "까지야."
            else:
                explain_text += "\n신청 기간은 잘 모르겠어."

        if schedule:
            if contests[0].contest_start and contests[0].contest_end:
                explain_text += "\n대회 시간은 " + contests[0].contest_start + "부터 " + contests[0].contest_end + "까지야."
            else:
                explain_text += "\n대회 시간은 잘 모르겠어"

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        print(f"contest_name : {contest_name}")

        return []


class ContestForm(FormAction):

    def name(self) -> Text:
        return "contest_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["contest_name"]

    def slot_mappings(self):
        return {
            "brief": [self.from_entity(entity="brief")],
            "detail": [self.from_entity(entity="detail")],
            "schedule": [self.from_entity(entity="schedule")],
            "reception_period": [self.from_intent(intent="reception_period", value=True)],
            "contest_name": [self.from_entity(entity="contest_name"), self.form_entity(entity="company")]
        }

    def validate_contest_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check contest_name"""

        print(f"contest_name {value}")
        return {"contest_name": value}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        return []


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
            "contest_name": [self.from_entity(entity="contest_name")],
            # , self.from_intent(intent="contest_name")],
            "level": [self.from_entity(entity="level"), self.from_intent(intent="level", value=True)],
            "number": [self.from_entity(entity="number")],
            # , self.from_intent(intent="number")],
            "algorithm_name": [self.from_entity(entity="algorithm_type"), self.from_entity(entity="algorithm_name")]
        }

    def validate_level(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check level"""
        # print(f"validate: ${tracker.get_latest_entity_values('brief_explain')}")
        print(f"level {value}")
        if (any(tracker.get_latest_entity_values('level'))):
            return {"level": value}
        else:
            # dispatcher.utter_message(template="utter_what_level")
            return {"level": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        return []


class ChangeForm(FormAction):

    def name(self) -> Text:
        return "change_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "problem_name": [self.from_entity(entity="problem_name")],
            "contest_name": [self.from_entity(entity="contest_name")],
            # , self.from_intent(intent="contest_name")],
            "level": [self.from_entity(entity="level"), self.from_intent(intent="level", value=True)],
            "number": [self.from_entity(entity="number")],
            # , self.from_intent(intent="number")],
            "algorithm_type": [self.from_entity(entity="algorithm_type")]
        }

    def validate_level_change(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check algorithm_type"""

        print(f"\nlevel change1 {value}")
        # print(f"validate: ${tracker.get_latest_entity_values('brief_explain')}")
        # print(f"level change {value}")
        #
        # level = tracker.get_slot('level')
        # #level change
        # if value.find('easy') != -1 :
        #     level = UserLevel.level_down(level)
        # elif value.find('hard') !=-1 :
        #     level = UserLevel.level_up(level)
        # tracker.set_slot("level",level)

        return {"level": value}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        return []
