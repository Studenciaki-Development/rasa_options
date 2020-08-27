def translate_entity_name_to_subcategory(subcategory):
    if subcategory == "1turn":
        subcategory = "Rozpoczęcie rekrutacji"
    elif subcategory == "2turn":
        subcategory = "Druga tura"
    elif subcategory == "limits":
        subcategory = "Limity przyjęć"
    elif subcategory == "courses":
        subcategory = "Lista kierunków"
    elif subcategory == "available":
        subcategory = "Wolne miejsca"
    elif subcategory == "recruitment_costs":
        subcategory = "Opłata rekrutacyjna"
    elif subcategory == "students_costs":
        subcategory = "Opłata za studia"
    elif subcategory == "returns":
        subcategory = "Zwrot opłat"
    return subcategory


def prepare_message(field_of_study, course_level, course_type, limit):
    if course_level is None and course_type == "stacjonarne":
        if limit["limit_stat1"] is None:
            course_level = "level2"
        if limit["limit_stat2"] is None:
            course_level = "level1"

    if course_level is None and course_type == "niestacjonarne":
        if limit["limit_niestat1"] is None:
            course_level = "level2"
        if limit["limit_niestat2"] is None:
            course_level = "level1"

    if course_type is None and course_level == "level1":
        if limit["limit_stat1"] is None:
            course_type = "niestacjonarne"
        if limit["limit_niestat1"] is None:
            course_type = "stacjonarne"

    if course_type is None and course_level == "level2":
        if limit["limit_stat2"] is None:
            course_type = "niestacjonarne"
        if limit["limit_niestat2"] is None:
            course_type = "stacjonarne"

    print_type = ""
    print_level = ""
    print_limit = 0
    if course_level == "level1" and course_type == "stacjonarne":
        print_type = "stacjonarnych"
        print_level = "pierwszego stopnia"
        print_limit = limit["limit_stat1"]
    elif course_level == "level2" and course_type == "stacjonarne":
        print_type = "stacjonarnych"
        print_level = "drugiego stopnia"
        print_limit = limit["limit_stat2"]
    elif course_level == "level1" and course_type == "niestacjonarne":
        print_type = "niestacjonarnych"
        print_level = "pierwszego stopnia"
        print_limit = limit["limit_niestat1"]
    elif course_level == "level2" and course_type == "niestacjonarne":
        print_type = "niestacjonarnych"
        print_level = "drugiego stopnia"
        print_limit = limit["limit_niestat2"]

    msg = f"Na {print_type} studiach {print_level} na kierunku {field_of_study} limit miejsc wynosi {print_limit}"
    return msg