import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from actions import db
from actions.func import level_up, level_down, level_mapping


class ActionLevelChangeEasy(Action):
    def name(self) -> Text:
        return "action_level_change_easy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        level = tracker.get_slot('problem_level')
        level_up(level_mapping(level))
        return [SlotSet('problem_level', level)]


class ActionLevelChangeHard(Action):
    def name(self) -> Text:
        return "action_level_change_hard"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        level = tracker.get_slot('problem_level')
        level_down(level_mapping(level))
        return [SlotSet('problem_level', level)]


class ActionAlgorithmExplain(FormAction):
    def name(self) -> Text:
        return "action_algorithm_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        brief = tracker.get_slot('brief')
        detail = tracker.get_slot('detail')
        level = tracker.get_slot('algorithm_level')
        algorithm_name = tracker.get_slot('algorithm_name')

        algorithms = db.get_algorithm_by_normalized_name(algorithm_name)
        buttons = []
        explain_text = ""

        if not algorithms:
            explain_text += "조건에 맞는 알고리즘이 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return []

        if algorithms and level:
            if algorithms[0].level:
                explain_text += f"\n난이도는 {algorithms[0].level}야"
            else:
                explain_text += f"\n난이도는 모르겠어."
            dispatcher.utter_message(text=explain_text)
            return [SlotSet("algorithm_level", None)]

        if algorithms and detail:
            if algorithms[0].detail_explain:
                explain_text += "이름 : " + algorithms[0].name
                explain_text += "\n" + algorithms[0].detail_explain
                buttons = [{"title": "간단한 설명",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "brief":"간단한"}}"""},
                           {"title": "난이도",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"난이도"}}"""},
                           {"title": "문제 추천",
                            "payload": f"""/problem_recommendation{{"algorithm_name:"{algorithm_name}"}}"""}]
            elif algorithms[0].brief_explain:
                explain_text += "이름 : " + algorithms[0].name
                explain_text += f"\n자세하게는 나도 모르겠어. 대신 간단하게 설명해줄게.\n{algorithms[0].brief_explain}"
                buttons = [{"title": "난이도",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"난이도"}}"""},
                           {"title": "문제 추천",
                            "payload": f"""/problem_recommendation{{"algorithm_name:"{algorithm_name}"}}"""}]
            else:
                explain_text += f"나도 잘 모르겠어.";
        elif algorithms:
            if algorithms[0].brief_explain:
                explain_text += "이름 : " + algorithms[0].name
                explain_text += "\n" + algorithms[0].brief_explain
                buttons = [{"title": "자세한 설명",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "detail":"자세한"}}"""},
                           {"title": "난이도",
                            "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"난이도"}}"""},
                           {"title": "문제 추천",
                            "payload": f"""/problem_recommendation{{"algorithm_name":"{algorithm_name}"}}"""}]
            else:
                explain_text += f"나도 잘 모르겠어.";

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        print(algorithms)
        print(f"detail : {detail}")
        print(f"brief : {brief}")
        print(f"level : {level}")
        print(f"algorithm_name : {algorithm_name}")

        return [SlotSet("brief", None), SlotSet("detail", None), SlotSet("algorithm_level", None)]


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
        level = level_mapping(tracker.get_slot('problem_level'))

        if number is None:
            number = 1
        ##이름, 알고리즘, 난이도, 대회이름
        problem = db.get_problem(problem_name, algorithm_name, level, contest_name, number)
        buttons = []
        explain_text = ""

        if not problem:
            explain_text += "조건에 맞는 문제가 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return [SlotSet("number", None), SlotSet("algorithm_name", None), SlotSet("contest_name", None), SlotSet("problem_level", None) ]

        algorithm_name = db.get_algorithm_name_by_problem(problem[0])
        print(algorithm_name)
        print(problem)

        if problem and contest_name:
            if problem[0].name:
                explain_text += "이름\n" + problem[0].name + "\n"
            else:
                explain_text += "이름 : 없음"
            if problem[0].uri:
                explain_text += "\n주소\n" + problem[0].uri + "\n"
            else:
                explain_text += "\n주소 : 없음"

            buttons = [{"title": "사용 알고리즘",
                        "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}'},
                       {"title": "대회",
                        "payload": f'/contest_explain{{"contest_name": "{contest_name}"}}'},
                       # {"title": "난이도",
                       #  "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"{난이도}"}}"""},
                       {"title": "다른 문제",
                        "payload": f'/problem_recommendation{{"algorithm_name":"{algorithm_name}"}}'}]
        elif problem and number:
            if problem[0].name:
                explain_text += "이름\n" + problem[0].name + "\n"
            else:
                explain_text += "이름 : 없음"
            if problem[0].uri:
                explain_text += "\n주소\n" + problem[0].uri + "\n"
            else:
                explain_text += "\n주소 : 없음"
            # 알고리즘 db에서 검색 후 모두 출력
            buttons = [{"title": "사용 알고리즘",
                        "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}"""},
                       # {"title": "난이도",
                       #  "payload": f"""/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"난이도"}}"""},
                       {"title": "다른 문제",
                        "payload": f"""/problem_recommendation{{"algorithm_name":"{algorithm_name}"}}"""}]

        if problem and level:
            if problem[0].level:
                explain_text += f"난이도는 {problem[0].level}야"
            else:
                explain_text += f"난이도 : 없음"

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        print(f"number : {number}")
        print(f"problem_name : {problem_name}")
        print(f"level : {level}")
        print(f"contest_name : {contest_name}")
        print(f"algorithm_name : {algorithm_name}")

        return [SlotSet("number", None)]


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
            "algorithm_level": [self.from_entity(entity="algorithm_level"),
                                self.from_intent(intent="algorithm_level", value=True)],
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
        return [SlotSet("problem_level", None), SlotSet("problem_name", None),
                SlotSet("contest_name", None), SlotSet("reception_period", None),
                SlotSet("homepage", None), SlotSet("schedule", None)]


class ActionContestExplain(FormAction):

    def name(self) -> Text:
        return "action_contest_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        past = tracker.get_slot('past')
        proceeding = tracker.get_slot('proceeding')

        reception_period = tracker.get_slot('reception_period')
        homepage = tracker.get_slot('homepage')
        schedule = tracker.get_slot('schedule')
        contest_name = tracker.get_slot('contest_name')

        contests = db.get_contest_by_normalized_name(contest_name)
        # contest를 시간순으로 정렬하고 필터링해서 출력한다.
        contests.sort(key=lambda x: x.contest_start)
        today = datetime.datetime.now()
        if past:
            contests = list(filter(lambda x: x.reception_end < today, contests))
        elif proceeding:
            contests = list(filter(lambda x: x.reception_start <= today <= x.reception_end, contests))

        explain_text = ""

        if not contests:
            explain_text += "조건에 맞는 대회가 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return []

        print(f"contest_name : {contest_name}")
        print(f"reception_period : {reception_period}")
        print(f"schedule : {schedule}")

        buttons = [{"title": "대회 정보",
                    "payload": f'/contest_explain{{"contest_name": "{contest_name}"}}'},
                   {"title": "대회 일정",
                    "payload": f'/contest_explain{{"contest_name": "{contest_name}", "schedule":"일정"}}'},
                   {"title": "대회 홈페이지",
                    "payload": f'/contest_explain{{"contest_name": "{contest_name}", "homepage":"홈페이지"}}'},
                   {"title": "신청 기간",
                    "payload": f'/contest_explain{{"contest_name": "{contest_name}", "reception_period": "신청 기간"}}'}]

        if homepage:
            if contests[0].name and contests[0].uri:
                explain_text = contests[0].name
                explain_text += "\n홈페이지 : " + contests[0].uri
            else:
                explain_text += "홈페이지 주소는 잘 모르곘어..."
            dispatcher.utter_message(text=explain_text, buttons=buttons)
            return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None)]

        if reception_period:
            if contests[0].reception_start and contests[0].reception_end:
                explain_text += "신청 기간은 " + contests[0].reception_start.strftime("%Y/%m/%d %H:%M") \
                                + "부터 " + contests[0].reception_end.strftime("%Y/%m/%d %H:%M") + "까지야."
            else:
                explain_text += "신청 기간은 잘 모르겠어."
            dispatcher.utter_message(text=explain_text, buttons=buttons)
            return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None)]

        if schedule:
            if contests[0].contest_start and contests[0].contest_end:
                explain_text += "대회 시간은 " + contests[0].contest_start.strftime("%Y/%m/%d %H:%M") \
                                + "부터 " + contests[0].contest_end.strftime("%Y/%m/%d %H:%M") + "까지야."
            else:
                explain_text += "대회 시간은 잘 모르겠어"
            dispatcher.utter_message(text=explain_text, buttons=buttons)
            return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None)]

        if contests:
            explain_text = contests[0].name

            if contests[0].reception_start and contests[0].reception_end:
                explain_text += "신청 기간은 " + contests[0].reception_start.strftime("%Y/%m/%d %H:%M") \
                                + "부터 " + contests[0].reception_end.strftime("%Y/%m/%d %H:%M") + "까지야."

            if contests[0].contest_start and contests[0].contest_end:
                explain_text += "대회 시간은 " + contests[0].contest_start.strftime("%Y/%m/%d %H:%M") \
                                + "부터 " + contests[0].contest_end.strftime("%Y/%m/%d %H:%M") + "까지야."

            if contests[0].uri:
                explain_text += "\n홈페이지 : " + contests[0].uri

            buttons = buttons[1:]
            dispatcher.utter_message(text=explain_text, buttons=buttons)

        return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None)]


class ContestForm(FormAction):
    def name(self) -> Text:
        return "contest_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["contest_name"]

    def slot_mappings(self):
        return {
            "schedule": [self.from_entity(entity="schedule"), self.from_intent(intent="schedule", value=True)],
            "homepage": [self.from_entity(entity="homepage"), self.from_intent(intent="homepage", value=True)],
            "reception_period": [self.from_entity(entity="reception_period"),
                                 self.from_intent(intent="reception_period", value=True)],
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
        return [SlotSet("brief", None), SlotSet("detail", None),
                SlotSet("problem_level", None), SlotSet("algorithm_level", None),
                SlotSet("algorithm_name", None), SlotSet("problem_name", None),
                SlotSet("number", None)]


class ProblemForm(FormAction):

    def name(self) -> Text:
        return "problem_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["problem_level"]

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
            "problem_level": [self.from_entity(entity="problem_level"),
                              self.from_intent(intent="problem_level", value=True)],
            "number": [self.from_entity(entity="number")],
            # , self.from_intent(intent="number")],
            "algorithm_name": [self.from_entity(entity="algorithm_name")]
        }

    def validate_problem_level(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check problem level"""

        print(f"problem_level {value}")
        return {"problem_level": value}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        return [SlotSet("brief", None), SlotSet("detail", None),
                SlotSet("code", None), SlotSet("algorithm_level", None),
                SlotSet("reception_period", None), SlotSet("homepage", None),
                SlotSet("schedule", None)]

# class ChangeForm(FormAction):
#
#     def name(self) -> Text:
#         return "change_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#
#     def slot_mappings(self):
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "problem_name": [self.from_entity(entity="problem_name")],
#             "contest_name": [self.from_entity(entity="contest_name")],
#             # , self.from_intent(intent="contest_name")],
#             "problem_level": [self.from_entity(entity="problem_level"),
#                               self.from_intent(intent="problem_level", value=True)],
#             "number": [self.from_entity(entity="number")],
#             # , self.from_intent(intent="number")],
#             "algorithm_name": [self.from_entity(entity="algorithm_name")]
#         }
#
#     def validate_level_change(
#             self,
#             value: Text,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         """check algorithm_type"""
#
#         print(f"\nlevel change1 {value}")
#         # print(f"validate: ${tracker.get_latest_entity_values('brief_explain')}")
#         # print(f"level change {value}")
#         #
#         # level = tracker.get_slot('level')
#         # #level change
#         # if value.find('easy') != -1 :
#         #     level = UserLevel.level_down(level)
#         # elif value.find('hard') !=-1 :
#         #     level = UserLevel.level_up(level)
#         # tracker.set_slot("level",level)
#
#         return {"problem_level": value}
#
#     def submit(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         # utter submit template
#         return []
