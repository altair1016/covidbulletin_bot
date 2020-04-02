"""
@name : file_check.py
@author: Marco Iannella (altair1016)
@desc: module with file and path naming rules
"""

import os
import datetime


def dir_exists(path):
    """
    Verify if target directory path exists, create it otherwise
    :param path: target directories path
    :return: boolean
    """
    try:
        os.makedirs(path)
        return False
    except FileExistsError:
        # directory already exists
        pass
    return True


def file_exists(path):
    """
    Verify if file exists
    :param path: target directories path
    :return: filename if exists else None
    """
    try:
        list_dir = os.listdir(path)
        rep_list = [' ', ':', '.', '-']
        fname = str(datetime.datetime.now())
        for elt in rep_list:
            fname = fname.replace(elt, "")
        token = fname[0:8]
        for elt in list_dir:
            if elt[0:8] == token:
                fname2 = elt
                raise FileExistsError
    except FileExistsError:
        # directory already exists
        return fname2
    return "None"


def file_naming_rules(path, last_elt):
    """
    Rename file following logics
    :param path: target directories path
    :return: path + filename
    """
    rep_list = [' ', ':', '.', '-']
    dir_exists(path)
    fname = str(datetime.datetime.now())
    for elt in rep_list:
        fname = fname.replace(elt, "")
        last_elt = last_elt.replace(elt, "")
    print(fname, last_elt)
    if fname[0:8] != last_elt[0:8]:
        fname = last_elt
    return path + "/" + fname + ".png"




