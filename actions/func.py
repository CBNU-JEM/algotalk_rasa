import logging

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


def level_down(level="실버"):
    le = ["브론즈", "실버", "골드", "플레티넘", "다이아", "루비"]
    if isinstance(level,int):
        if level > 5:
            level = level - 5

    return le[level/5]


def level_up(level="실버"):
    le = ["브론즈", "실버", "골드", "플레티넘", "다이아", "루비"]
    if isinstance(level,int):
        if level < 22:
            level = level + 5

    return le[level/5]


changed_level = dict()
# key = ["브론즈", "실버", "골드", "플레티넘", "플레", "다이아", "상", "중", "하", "초급", "중급", "고급", "쉬움", "쉬운", "쉬운거", "쉬운 것", "어려움",
#       "어려운거", "어려운 것", "어려운"]
# value = ["브론즈", "실버", "골드", "플레티넘", "플레티넘", "다이아", "플레티넘", "골드", "실버", "실버", "골드", "플레티넘", "실버", "실버", "실버", "실버",
#         "플레티넘", "플레티넘", "플레티넘", "플레티넘"]

key = ["랜덤", "브론즈", "실버", "골드", "플레티넘", "다이아", "루비"]
value = [0, 1, 6, 11, 16, 21, 26]

for i in range(len(key)):
    changed_level[key[i]] = value[i]


def slot_level_mapping(level):
    if not level:
        return 0

    if level.isdigit():
        return level

    print(changed_level.get(level, 0))
    return changed_level.get(level, 0)


def level_num_to_string(level):
    if level == 0:
        return "없음"

    if not level or isinstance(level, str):
        return "없음"

    logger.info(f'level_mapping_string : {level}')

    changed_level_string = dict()
    key = [0, 1, 2, 3, 4, 5]
    value = ["브론즈", "실버", "골드", "플레티넘", "다이아", "루비"]

    for i in range(len(key)):
        changed_level_string[key[i]] = value[i]

    logger.info(f'level_mapping_string : {(level - 1) // 5}')
    ret = changed_level_string.get((level - 1) // 5, "없음") + str((level - 1) % 5 + 1)
    return ret


def slot_level_num_to_string(level):
    logger.info(f'slot_level_num_to_string : {level}')
    if level == 0:
        return "랜덤"
    changed_level_string = dict()
    key = [0, 1, 2, 3, 4, 5]
    value = ["브론즈", "실버", "골드", "플레티넘", "다이아", "루비"]

    for i in range(len(key)):
        changed_level_string[key[i]] = value[i]

    logger.info(f'level_mapping_string : {level}')
    ret = changed_level_string.get((level - 1) // 5, "랜덤")
    return ret


def level_explain(level):
    if "브론즈" in level:
        return "(기초 개념 공부할때)\n"
    elif "실버" in level:
        return "(쉬운 코테 수준)\n"
    elif "골드" in level:
        return "(어려운 코테 수준)\n"
    elif "플레티넘" in level:
        return "(알고리즘 심화 응용 수준)\n"
    elif "다이아" in level:
        return "(고수들만 도전)\n"
    elif "루비" in level:
        return "(초고수들만 도전)\n"
    else:
        return ""

class OverlapProblem:
    def __init__(self, problem=None):
        self.problem = problem
