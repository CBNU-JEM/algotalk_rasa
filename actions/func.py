def level_down(level="실버"):
    le = ["브론즈", "실버", "골드", "플레티넘", "다이아"]
    for i, v in enumerate(le):
        if v.find(level) != -1:
            idx = i - 1 if i > 0 else i
            return le[idx]
    return level


def level_up(level="실버"):
    le = ["브론즈", "실버", "골드", "플레티넘", "다이아"]
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

key = ["브론즈", "실버", "골드", "플레티넘", "다이아"]
value = [1, 6, 11, 16, 21]

for i in range(len(key)):
    changed_level[key[i]] = value[i]


def level_mapping(level):
    print(changed_level.get(level, 0))
    return changed_level.get(level, 0)


class OverlapProblem:
    def __init__(self, problem=None):
        self.problem = problem
