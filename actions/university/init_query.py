from .queries.queries import get_categories
from ..university.translate import translate_entity_name_to_subcategory


def init_query(selected_category, subcategory):
    if subcategory is not None:
        subcategory = translate_entity_name_to_subcategory(subcategory)
        subcategory_list = get_categories(subcategory)
    elif selected_category is not None:
        subcategory_list = get_categories(selected_category)
    else:
        subcategory_list = get_categories("root")

    return subcategory_list
