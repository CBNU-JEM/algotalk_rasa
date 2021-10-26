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
from actions.func import level_up, level_down, slot_level_mapping, level_num_to_string

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
        level_up(slot_level_mapping(level))
        return [SlotSet('problem_level', level)]


class ActionLevelChangeHard(Action):
    def name(self) -> Text:
        return "action_level_change_hard"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        level = tracker.get_slot('problem_level')
        level_down(slot_level_mapping(level))
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

        problem_name = tracker.get_slot('problem_name')

        logger.info(f"detail : {detail}")
        logger.info(f"level : {level}")
        logger.info(f"algorithm_name : {algorithm_name}")
        logger.info(f"problem_name : {problem_name}")

        algorithms = []
        if problem_name:
            algorithms = db.find_algorithm_name_by_problem(problem_name)
        else:
            algorithms = db.find_algorithm_by_normalized_name(algorithm_name)
        logger.info(algorithms)

        explain_text = ""
        search_text = ""
        if not algorithms:
            explain_text += "조건에 맞는 알고리즘이 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return [AllSlotsReset()]

        # algorithm = random.choice(algorithms)

        logger.info(f"choice algorithm level : {level}")
        # logger.info(f"choice algorithm name : {algorithm.name}")
        algorithms_dict = []

        for algorithm in algorithms:
            buttons = []
            explain_text = ""
            if problem_name:
                search_text = f"{problem_name}으로 검색한 알고리즘"


            if detail:
                if algorithm.detail_explain:

                    explain_text += f"{algorithm.name}\n"
                    explain_text += f"\n{algorithm.detail_explain}\n"
                    buttons = [{"title": "간단한 설명",
                                "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm.name}"}}'},
                               {"title": "난이도",
                                "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm.name}", "algorithm_level":"난이도"}}'},
                               {"title": "문제 추천",
                                "payload": f'/problem_recommendation{{"algorithm_name:"{algorithm.name}"}}'}]
                elif algorithm.brief_explain:
                    explain_text += f"{algorithm.name}\n"
                    explain_text += f"\n자세하게는 나도 모르겠어. 대신 간단하게 설명해줄게.\n{algorithm.brief_explain}\n"
                    buttons = [{"title": "난이도",
                                "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm.name}", "algorithm_level":"난이도"}}'},
                               {"title": "문제 추천",
                                "payload": f'/problem_recommendation{{"algorithm_name:"{algorithm.name}"}}'}]
                else:
                    explain_text += f"나도 잘 모르겠어.";
            else:

                if algorithm.brief_explain:
                    explain_text += f"{algorithm.name}\n"
                    explain_text += f"\n{algorithm.brief_explain}\n"
                    buttons = [{"title": "자세한 설명",
                                "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm.name}", "detail":"자세한"}}'},
                               {"title": "난이도",
                                "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm.name}", "algorithm_level":"난이도"}}'},
                               {"title": "문제 추천",
                                "payload": f'/problem_recommendation{{"algorithm_name":"{algorithm.name}"}}'}]
                else:
                    explain_text += f"나도 잘 모르겠어.";
            if level:
                if algorithm.level:
                    explain_text += f"\n난이도 : {algorithm.level}"
                else:
                    explain_text += f"\n난이도는 모르겠어."

                buttons = [{"title": "간단한 설명",
                            "payload": f'/algorithm_explain{{"algorithm_name": "{algorithm.name}"}}'},
                           {"title": "문제 추천",
                            "payload": f'/problem_recommendation{{"algorithm_name:"{algorithm.name}"}}'}]

            algorithms_dict.append({"text": explain_text, "buttons": buttons})
            if len(algorithms_dict) == 5:
                break

        algorithms_json = {"list": algorithms_dict}
        if search_text:
            dispatcher.utter_message(text=search_text, json_message=algorithms_json)
        else:
            dispatcher.utter_message(json_message=algorithms_json)

        return [SlotSet("detail", None), SlotSet("algorithm_level", None), SlotSet("problem_name", None)]


class ActionProblemRecommended(FormAction):
    def name(self) -> Text:
        return "action_problem_recommended"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info("----------problem recommand-----------\n")
        logger.info(tracker.latest_message)

        logger.info(f"problem sender : {tracker.sender_id}")

        algorithm_name = tracker.get_slot('algorithm_name')
        number = tracker.get_slot('number')
        problem_name = tracker.get_slot('problem_name')
        level = slot_level_mapping(tracker.get_slot('problem_level'))

        logger.info(f"slot algorithm_name : {algorithm_name}")
        logger.info(f"slot number : {number}")
        logger.info(f"slot problem_name : {problem_name}")
        logger.info(f"slot problem_level : {tracker.get_slot('problem_level')}")
        logger.info(f"level_mapping : {level}")

        if number is None:
            number = 5

        if level is None:
            level = 0

        ##이름, 알고리즘, 난이도
        problems = db.find_problem(problem_name, algorithm_name, level, number)

        if not problems:
            explain_text = "조건에 맞는 문제가 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return [AllSlotsReset()]

        search_text = ""
        problems_dict = []
        if level:
            level_string = level_num_to_string(level)
            if level_string == "없음":
                level_string = "랜덤"
            search_text += f"난이도가 {level_string}인 {level_explain(level)}"

        if problem_name:
            search_text += f"{problem_name}으로 검색한 문제"

        for problem in problems:
            explain_text = ""
            algorithm_name = db.find_algorithm_name_by_problem(problem)

            logger.info(f"problem's algorithm_name : {algorithm_name}")
            logger.info(f"choice problem_name : {problem.name}")

            if problem.name:
                explain_text += problem.name + "\n"
            else:
                explain_text += "이름 : 없음\n"

            if problem.level:
                explain_text += f"\n난이도 : {level_num_to_string(problem.level)}\n"
            else:
                explain_text += "\n난이도 : 없음\n"

            if problem.uri:
                explain_text += f"\n홈페이지 : {problem.uri}"
            else:
                explain_text += "\n홈페이지 : 없음"

            buttons = [{"title": "사용 알고리즘",
                        "payload": f'/algorithm_explain{{"problem_name": "{problem.name}"}}'},
                       {"title": "다른 문제",
                        "payload": f'/problem_recommendation{{ }}'},
                       {"title": "다른 난이도 문제",
                        "payload": f'/problem_recommendation{{"problem_level": null}}'}]

            problems_dict.append({"text": explain_text, "buttons": buttons})

            if len(problems_dict) == 5:
                break

        logger.info(f"problems_json : {problems_dict}")
        problems_json = {"list": problems_dict}

        if search_text:
            dispatcher.utter_message(text=search_text, json_message=problems_json)
        else:
            dispatcher.utter_message(json_message=problems_json)

        return [SlotSet("number", None)]


class AlgorithmForm(FormAction):

    def name(self) -> Text:
        return "algorithm_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["algorithm_name"]

    def slot_mappings(self):
        return {
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

        search_text = ""
        contests = []
        if contest_name:
            contests = db.find_contest_by_normalized_name(contest_name)

            today = datetime.datetime.now()
            if past:
                search_text += "신청기간이 지난 "
                contests = list(filter(lambda x: x.reception_end < today, contests))
            elif proceeding:
                search_text += "접수가 진행중인 "
                contests = list(filter(lambda x: x.reception_start <= today and today <= x.reception_end, contests))
            elif expected:
                search_text += "곧 접수가 시작될 "
                contests = list(filter(lambda x: x.reception_start > today, contests))
            else:
                search_text += "대회가 끝나지 않은 "
                contests = list(filter(lambda x: x.contest_end > today, contests))

            search_text += f"{contest_name}으로 검색한 대회"
        else:
            if past:
                search_text += "신청기간이 지난 모든 대회"
                contests = db.find_last_contests()
            elif proceeding:
                search_text += "접수가 진행중인 모든 대회"
                contests = db.find_contests_in_proceeding()
            elif expected:
                search_text += "곧 접수가 시작될 모든 대회"
                contests = db.find_expected_contests()
            else:
                search_text += "대회가 끝나지 않은 모든 대회"
                contests = db.find_unfinished_contests()

        logger.info(f"contests : {contests}")

        if not contests:
            explain_text = "조건에 맞는 대회가 없는거같아..."
            dispatcher.utter_message(text=explain_text)
            return [AllSlotsReset()]

        contests_dict = []

        for contest in contests:
            explain_text = ""
            buttons = [{"title": "상세 정보",
                        "payload": f'/contest_explain{{"contest_name": "{contest.name}"}}'},
                       {"title": "일정",
                        "payload": f'/contest_explain{{"contest_name": "{contest.name}", "schedule":"일정"}}'},
                       {"title": "홈페이지",
                        "payload": f'/contest_explain{{"contest_name": "{contest.name}", "homepage":"홈페이지"}}'}]

            if homepage or schedule:
                if schedule:
                    search_text += " 일정"
                    if contest.name:
                        explain_text = contest.name + '\n'

                    if contest.reception_start and contest.reception_end:
                        explain_text += f"\n신청 기간 : {contest.reception_start.strftime('%Y/%m/%d %H:%M')} ~ {contest.reception_end.strftime('%Y/%m/%d %H:%M')}"
                    else:
                        explain_text += "\n신청 기간 : 정보 없음"

                    if contest.contest_start and contest.contest_end:
                        explain_text += f"\n대회 기간 : {contest.contest_start.strftime('%Y/%m/%d %H:%M')} ~ {contest.contest_end.strftime('%Y/%m/%d %H:%M')}"
                    else:
                        explain_text += "\n대회 시간 : 정보 없음"

                if homepage:
                    if schedule:
                        explain_text += '\n'
                        search_text += "과 홈페이지"
                    else:
                        search_text += " 홈페이지"

                    if contest.name and contest.uri:
                        explain_text = contest.name + '\n'
                        explain_text += f"\n홈페이지 : {contest.uri}"
                    else:
                        explain_text += "\n홈페이지 : 정보 없음"
            else:
                if contest.name:
                    explain_text = contest.name + '\n'

                if contest.reception_start and contest.reception_end:
                    explain_text += f"\n신청 기간 : {contest.reception_start.strftime('%Y/%m/%d %H:%M')} ~ {contest.reception_end.strftime('%Y/%m/%d %H:%M')}\n"

                if contest.contest_start and contest.contest_end:
                    explain_text += f"\n대회 기간 : {contest.contest_start.strftime('%Y/%m/%d %H:%M')} ~ {contest.contest_end.strftime('%Y/%m/%d %H:%M')}\n"

                if contest.uri:
                    explain_text += f"\n홈페이지 : {contest.uri}"

                buttons = buttons[1:]

            contests_dict.append({"text": explain_text, "buttons": buttons})

            if len(contests_dict) == 5:
                break

        logger.info(f"contests_json : {contests_dict}")
        contests_json = {"list": contests_dict}

        dispatcher.utter_message(text=search_text, json_message=contests_json)

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
            "contest_name": [self.from_entity(entity="contest_name"), self.from_entity(entity="company")],
            "schedule": [self.from_entity(entity="schedule"), self.from_entity(entity="reception_period"),
                         self.from_intent(intent="schedule", value=True),
                         self.from_intent(intent="reception_period", value=True)]
        }

    def validate_contest_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check contest_name"""

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
        return ["problem_level"]

    def slot_mappings(self):
        return {
            "problem_level": [self.from_entity(entity="problem_level"),
                              self.from_intent(intent="problem_level", value="problem_level")],
            "number": [self.from_entity(entity="number"), self.from_intent(intent="number", value=True)]
        }

    def validate_problem_level(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """check problem level"""

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
