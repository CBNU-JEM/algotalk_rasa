
class UserLevel:
    def __init__(self, level="브론즈"):
        self.level=level

    def level_down(self,level):
        le=["브론즈","실버","골드","플레티넘","다이아"]
        for i,v in enumerate(le):
            if v.find(level) != -1:
                idx=i-1 if i>0 else i
                return le[idx]
        return le[0]
    def level_up(self,level):
        le=["브론즈","실버","골드","플레티넘","다이아"]
        for i,v in enumerate(le):
            if v.find(level) != -1:
                idx=i+1 if i<4 else i
                return le[idx]
        return le[0]


class OverlapProblem:
    def __init__(self, problem=None):
        self.problem=problem
