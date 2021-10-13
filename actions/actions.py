import datetime
import logging
import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from actions import db
from actions.func import level_up, level_down, level_mapping

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


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

        logger.info("----------algorithm explain-----------\n")

        detail = tracker.get_slot('detail')
        level = tracker.get_slot('algorithm_level')
        algorithm_name = tracker.get_slot('algorithm_name')

        logger.info(f"detail : {detail}")
        logger.info(f"level : {level}")
        logger.info(f"algorithm_name : {algorithm_name}")
        
        algorithms = db.get_algorithm_by_normalized_name(algorithm_name)
        logger.info(algorithms)
        
        buttons = []
        explain_text = ""

        if not algorithms:
            explain_text += "조건에 맞는 알고리즘이 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return [AllSlotsReset()]

        algorithm = random.choice(algorithms)

        if level:
            if algorithm.level:
                explain_text += f"\n난이도 : {algorithm.level}"
            else:
                explain_text += f"\n난이도는 모르겠어."

            buttons = [{"title": "간단한 설명",
                        "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}'},
                       {"title": "문제 추천",
                        "payload": f'/problem_recommendation{{"algorithm_name:"{algorithm_name}"}}'}]
            dispatcher.utter_message(text=explain_text, buttons=buttons)
            return [SlotSet("algorithm_level", None)]

        if detail:
            if algorithm.detail_explain:
                explain_text += "이름 : " + algorithm.name
                explain_text += "\n" + algorithm.detail_explain
                buttons = [{"title": "간단한 설명",
                            "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}'},
                           {"title": "난이도",
                            "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"난이도"}}'},
                           {"title": "문제 추천",
                            "payload": f'/problem_recommendation{{"algorithm_name:"{algorithm_name}"}}'}]
            elif algorithm.brief_explain:
                explain_text += "이름 : " + algorithm.name
                explain_text += f"\n자세하게는 나도 모르겠어. 대신 간단하게 설명해줄게.\n{algorithm.brief_explain}"
                buttons = [{"title": "난이도",
                            "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"난이도"}}'},
                           {"title": "문제 추천",
                            "payload": f'/problem_recommendation{{"algorithm_name:"{algorithm_name}"}}'}]
            else:
                explain_text += f"나도 잘 모르겠어.";
        else:
            if algorithm.brief_explain:
                explain_text += "이름 : " + algorithm.name
                explain_text += "\n" + algorithm.brief_explain
                buttons = [{"title": "자세한 설명",
                            "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}", "detail":"자세한"}}'},
                           {"title": "난이도",
                            "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}", "algorithm_level":"난이도"}}'},
                           {"title": "문제 추천",
                            "payload": f'/problem_recommendation{{"algorithm_name":"{algorithm_name}"}}'}]
            else:
                explain_text += f"나도 잘 모르겠어.";

        dispatcher.utter_message(text=explain_text, buttons=buttons)

        return [SlotSet("detail", None), SlotSet("algorithm_level", None)]


class ActionProblemRecommended(FormAction):
    def name(self) -> Text:
        return "action_problem_recommended"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info("----------problem recommand-----------\n")
        logger.info(tracker.latest_message)

        algorithm_name = tracker.get_slot('algorithm_name')
        number = tracker.get_slot('number')
        problem_name = tracker.get_slot('problem_name')
        contest_name = tracker.get_slot('contest_name')
        level = level_mapping(tracker.get_slot('problem_level'))

        logger.info(f"slot algorithm_name : {algorithm_name}")
        logger.info(f"slot number : {number}")
        logger.info(f"slot problem_name : {problem_name}")
        logger.info(f"slot contest_name : {contest_name}")
        logger.info(f"slot problem_level : {tracker.get_slot('problem_level')}")
        logger.info(f"level_mapping : {level}")

        if number is None:
            number = 1

        if level is None:
            level = 0

        ##이름, 알고리즘, 난이도, 대회이름
        problems = db.get_problem(problem_name, algorithm_name, level, number)

        buttons = []
        explain_text = ""

        if not problems:
            explain_text += "조건에 맞는 문제가 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return [AllSlotsReset()]
        
        problem = random.choice(problems)
        
        algorithm_name = db.get_algorithm_name_by_problem(problem)


        if contest_name:
            if problem.name:
                explain_text += "이름\n" + problem.name + "\n"
            else:
                explain_text += "이름 : 없음"
            if problem.uri:
                explain_text += "\n홈페이지\n" + problem.uri + "\n"
            else:
                explain_text += "\n홈페이지 : 없음"

            buttons = [{"title": "사용 알고리즘",
                        "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}'},
                       {"title": "대회",
                        "payload": f'/contest_explain{{"contest_name": "{contest_name}"}}'},
                       {"title": "다른 문제",
                        "payload": f'/problem_recommendation{{ }}'},
                       {"title": "다른 난이도 문제",
                        "payload": f'/problem_recommendation{{"problem_level": null}}'}]
        elif number:
            if problem.name:
                explain_text += "이름\n" + problem.name + "\n"
            else:
                explain_text += "이름 : 없음"
            if problem.uri:
                explain_text += "\n홈페이지\n" + problem.uri + "\n"
            else:
                explain_text += "\n홈페이지 : 없음"
            # 알고리즘 db에서 검색 후 모두 출력
            buttons = [{"title": "사용 알고리즘",
                        "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm_name}"}}'},
                       {"title": "다른 문제",
                        "payload": f'/problem_recommendation{{ }}'},
                       {"title": "다른 난이도 문제",
                        "payload": f'/problem_recommendation{{"problem_level": null}}'}]

        if problem.level:
            explain_text += f"난이도 : {level_mapping_string(problem.level)}"
        else:
            explain_text += f"난이도 : 없음"

        dispatcher.utter_message(text=explain_text, buttons=buttons)

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
                SlotSet("homepage", None), SlotSet("schedule", None),
                SlotSet("past", None), SlotSet("proceeding", None),
                SlotSet("expected", None)]


class ActionContestExplain(FormAction):

    def name(self) -> Text:
        return "action_contest_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logger.info("----------contest explain-----------\n")
        past = tracker.get_slot('past')
        proceeding = tracker.get_slot('proceeding')
        expected = tracker.get_slot('expected')

        reception_period = tracker.get_slot('reception_period')
        homepage = tracker.get_slot('homepage')
        schedule = tracker.get_slot('schedule')
        contest_name = tracker.get_slot('contest_name')

        logger.info(f"contest_name : {contest_name}")
        logger.info(f"past : {past}")
        logger.info(f"proceeding : {proceeding}")
        logger.info(f"expected : {expected}")
        logger.info(f"reception_period : {reception_period}")
        logger.info(f"schedule : {schedule}")

        contests = db.get_contests()
        # contest를 시간순으로 정렬하고 필터링해서 출력한다.
        contests.sort(key=lambda x: x.reception_start)

        today = datetime.datetime.now()
        if past:
            contests = list(filter(lambda x: x.reception_end < today, contests))
        elif proceeding:
            contests = list(filter(lambda x: x.reception_start <= today <= x.reception_end, contests))
        elif expected:
            contests = list(filter(lambda x: today < x.reception_start, contests))
        else:
            contests = list(filter(lambda x: today < x.contest_end, contests))


        if contest_name:
            contests = list(filter(lambda x: db.normalize(contest_name) in x.normalized_name, contests))

        explain_text = ""

        if not contests:
            explain_text += "조건에 맞는 대회가 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return [AllSlotsReset()]

        contest = random.choice(contests)

        buttons = [{"title": "상세 정보",
                    "payload": f'/contest_explain{{"contest_name": "{contest.name}"}}'},
                   {"title": "일정",
                    "payload": f'/contest_explain{{"contest_name": "{contest.name}", "schedule":"일정"}}'},
                   {"title": "홈페이지",
                    "payload": f'/contest_explain{{"contest_name": "{contest.name}", "homepage":"홈페이지"}}'},
                   {"title": "신청 기간",
                    "payload": f'/contest_explain{{"contest_name": "{contest.name}", "reception_period": "신청 기간"}}'}]


        if homepage:
            if contests[0].name and contests[0].uri:
                explain_text = contests[0].name + '\n'
                explain_text += "\n홈페이지 : " + contests[0].uri
            else:
                explain_text += "\n홈페이지 : 정보 없음"
            dispatcher.utter_message(text=explain_text, buttons=buttons)
            return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None),
                    SlotSet("past", None), SlotSet("proceeding", None), SlotSet("expected", None)]

        if reception_period:
            if contests[0].name:
                explain_text = contests[0].name + '\n'
            if contests[0].reception_start and contests[0].reception_end:
                explain_text += "\n신청 기간 : " + contests[0].reception_start.strftime("%Y/%m/%d %H:%M") \
                                + " ~ " + contests[0].reception_end.strftime("%Y/%m/%d %H:%M")
            else:
                explain_text += "\n신청 기간 : 정보 없음"
            dispatcher.utter_message(text=explain_text, buttons=buttons)
            return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None),
                    SlotSet("past", None), SlotSet("proceeding", None), SlotSet("expected", None)]

        if schedule:
            if contests[0].name:
                explain_text = contests[0].name + '\n'
            if contests[0].contest_start and contests[0].contest_end:
                explain_text += "\n대회 시간 : " + contests[0].contest_start.strftime("%Y/%m/%d %H:%M") \
                                + " ~ " + contests[0].contest_end.strftime("%Y/%m/%d %H:%M")
            else:
                explain_text += "\n대회 시간 : 정보 없음"
            dispatcher.utter_message(text=explain_text, buttons=buttons)
            return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None),
                    SlotSet("past", None), SlotSet("proceeding", None), SlotSet("expected", None)]

        if contests:
            if contests[0].name:
                explain_text = contests[0].name + '\n'

            if contests[0].reception_start and contests[0].reception_end:
                explain_text += "\n신청 기간은 " + contests[0].reception_start.strftime("%Y/%m/%d %H:%M") \
                                + "부터 " + contests[0].reception_end.strftime("%Y/%m/%d %H:%M") + "까지야."

            if contests[0].contest_start and contests[0].contest_end:
                explain_text += "\n대회 시간은 " + contests[0].contest_start.strftime("%Y/%m/%d %H:%M") \
                                + "부터 " + contests[0].contest_end.strftime("%Y/%m/%d %H:%M") + "까지야."

            if contests[0].uri:
                explain_text += "\n홈페이지 : " + contests[0].uri

            buttons = buttons[1:]
            dispatcher.utter_message(text=explain_text, buttons=buttons)

        return [SlotSet("homepage", None), SlotSet("reception_period", None), SlotSet("schedule", None),
                SlotSet("past", None), SlotSet("proceeding", None), SlotSet("expected", None)]


class ContestForm(FormAction):
    def name(self) -> Text:
        return "contest_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return []

    def slot_mappings(self):
        return {
            "schedule": [self.from_entity(entity="schedule"), self.from_intent(intent="schedule", value=True)],
            "homepage": [self.from_entity(entity="homepage"), self.from_intent(intent="homepage", value=True)],
            "reception_period": [self.from_entity(entity="reception_period"),
                                 self.from_intent(intent="reception_period", value=True)],
            "contest_name": [self.from_entity(entity="contest_name"), self.from_entity(entity="company")]
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
        return [SlotSet("detail", None), SlotSet("problem_level", None),
                SlotSet("algorithm_level", None), SlotSet("algorithm_name", None),
                SlotSet("problem_name", None), SlotSet("number", None)]


class ProblemForm(FormAction):

    def name(self) -> Text:
        return "problem_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        logger.info("----------required_slots-----------\n")
        logger.info(f"problem_level : {tracker.get_slot('problem_level')}\n")
        logger.info(f"reset_problem_level : {tracker.get_slot('reset_problem_level')}\n")

        return ["problem_level"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "problem_name": [self.from_entity(entity="problem_name")],
            # , self.from_intent(intent="contest_name")],
            "problem_level": [self.from_entity(entity="problem_level"),
                              self.from_intent(intent="problem_level", value="problem_level")],
            "number": [self.from_entity(entity="number")],
            # , self.from_intent(intent="number")],
            "algorithm_name": [self.from_entity(entity="algorithm_name")],
            "reset_problem_level": [self.from_entity(entity="reset_problem_level")],
            "past": [self.from_entity(entity="past")],
            "proceeding": [self.from_entity(entity="proceeding")],
            "expected": [self.from_entity(entity="expected")]
        }

    def validate_problem_level(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check problem level"""

        logger.info("\n----------problem level confirm-----------\n")
        logger.info(f"problem_level {value}")

        return {"problem_level": value}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        return [SlotSet("detail", None), SlotSet("algorithm_level", None), SlotSet("reception_period", None),
                SlotSet("homepage", None), SlotSet("schedule", None), SlotSet("past", None),
                SlotSet("proceeding", None), SlotSet("expected", None)]
