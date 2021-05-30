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

# def level_mapping(level):
#     le = ["브론즈", "실버", "골드", "플레티넘", "다이아"]
#     for i, v in enumerate(le):
#         if v.find(level) != -1:
#             idx = i + 1 if i < 4 else i
#             return le[idx]
#     return


class OverlapProblem:
    def __init__(self, problem=None):
        self.problem = problem
