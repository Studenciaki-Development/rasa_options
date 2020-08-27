def translate_entity_name_to_subcategory(subcategory):
    if subcategory == '1turn':
        subcategory = "Rozpoczęcie rekrutacji"
    elif subcategory== "2turn":
        subcategory = "Druga tura"
    elif subcategory== "limits":
        subcategory = "Limity przyjęć"
    elif subcategory== "courses":
        subcategory = "Lista kierunków"
    elif subcategory== "available":
        subcategory = "Wolne miejsca"
    elif subcategory== "recruitment_costs":
        subcategory = "Opłata rekrutacyjna"
    elif subcategory== "students_costs":
        subcategory = "Opłata za studia"
    elif subcategory== "returns":
        subcategory = "Zwrot opłat"
    return subcategory