def is_only_stationary(limit_niestat1, limit_niestat2):
    if limit_niestat1 is None and limit_niestat2 is None:
        return True
    else:
        return False


def is_only_first_degree(limit_stat2, limit_niestat2):
    if limit_stat2 is None and limit_niestat2 is None:
        return True
    else:
        return False


def is_only_second_degree(limit_stat1, limit_niestat1):
    if limit_stat1 is None and limit_niestat1 is None:
        return True
    else:
        return False


def is_only_non_stationary(limit_stat1, limit_stat2):
    if limit_stat1 is None and limit_stat2 is None:
        return True
    else:
        return False


def verify_limits(limits):
    if is_only_stationary(limits["limit_niestat1"], limits["limit_niestat2"]):
        return ["field-of-study", "course-level"]
    elif is_only_first_degree(limits["limit_stat2"], limits["limit_niestat2"]):
        return ["field-of-study", "course-type"]
    elif is_only_non_stationary(limits["limit_stat1"], limits["limit_stat2"]):
        return ["field-of-study", "course-level"]
    else:
        return ["field-of-study", "course-level", "course-type"]