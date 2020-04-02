"""
@name : region_district_check.py.py
@author: Marco Iannella (altair1016)
Module for string comparisons
"""
def check_value(user_insert, default_values):
    """
    Compares input
    :param user_insert: String inserted by user
    :param default_values: List of values to be compared
    :return: element if exist, NULL otherwise
    """
    rep_list = [' ', ':', '.', '-', ',' , '!', '?']
    for elt in user_insert:
        if elt in rep_list:
            user_insert.replace(elt, "")
    for elt in default_values:
        if user_insert.split(" ")[0].lower() in elt.lower():
            if len(user_insert.split(" ")[0].lower()) != len(elt.lower()):
                return "NULL"
            return elt.lower()
    return "NULL"
