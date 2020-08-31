def isOnlyStationary(limit_niestat1, limit_niestat2):
    if limit_niestat1 is None and limit_niestat2 is None:
        return True
    else:
        return False


def isOnlyFirstDegree(limit_stat2, limit_niestat2):
    if limit_stat2 is None and limit_niestat2 is None:
        return True
    else:
        return False


def isOnlySecondtDegree(limit_stat1, limit_niestat1):
    if limit_stat1 is None and limit_niestat1 is None:
        return True
    else:
        return False


def isOnlyNonStationary(limit_stat1, limit_stat2):
    if limit_stat1 is None and limit_stat2 is None:
        return True
    else:
        return False


def verify_limits(limits):
    if isOnlyStationary(limits["limit_niestat1"], limits["limit_niestat2"]):
        return ["field-of-study", "course-level"]
    elif isOnlyFirstDegree(limits["limit_stat2"], limits["limit_niestat2"]):
        return ["field-of-study", "course-type"]
    elif isOnlyNonStationary(limits["limit_stat1"], limits["limit_stat2"]):
        return ["field-of-study", "course-level"]
    else:
        return ["field-of-study", "course-level", "course-type"]