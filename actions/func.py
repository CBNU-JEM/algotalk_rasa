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
    for i, v in enumerate(le):
        if v.find(level) != -1:
            idx = i - 1 if i > 0 else i
            return le[idx]
    return level


def level_up(level="실버"):
    le = ["브론즈", "실버", "골드", "플레티넘", "다이아", "루비"]
    for i, v in enumerate(le):
        if v.find(level) != -1:
            idx = i + 1 if i < 4 else i
            return le[idx]
    return level


changed_level = dict()
# key = ["브론즈", "실버", "골드", "플레티넘", "플레", "다이아", "상", "중", "하", "초급", "중급", "고급", "쉬움", "쉬운", "쉬운거", "쉬운 것", "어려움",
#       "어려운거", "어려운 것", "어려운"]
# value = ["브론즈", "실버", "골드", "플레티넘", "플레티넘", "다이아", "플레티넘", "골드", "실버", "실버", "골드", "플레티넘", "실버", "실버", "실버", "실버",
#         "플레티넘", "플레티넘", "플레티넘", "플레티넘"]

key = ["브론즈", "실버", "골드", "플레티넘", "다이아", "루비"]
value = [1, 6, 11, 16, 21, 26]

for i in range(len(key)):
    changed_level[key[i]] = value[i]


def level_mapping(level):
    if not level:
        return 0

    if level.isdigit():
        return level

    print(changed_level.get(level, 0))
    return changed_level.get(level, 0)


def level_mapping_string(level):
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


class OverlapProblem:
    def __init__(self, problem=None):
        self.problem = problem
