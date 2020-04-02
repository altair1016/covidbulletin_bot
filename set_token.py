"""
@name : set_token.py
@author: Marco Iannella (altair1016)
Module to get json setup tokens
"""

import sys
import json

class SetToken:
    __token__ = ""
    __secret__ = ""

    def __init__(self):
        with open("setup.json", "rb") as r:
            try:
                jsonVars = json.load(r)
                self.__token__ = jsonVars['tokenID']
                self.__secret__ = jsonVars['secretID']

            except:
                print("Error in var names")
                sys.exit(0)

    def get_token(self):
        """
        Get and config telegram token
        :return: Telegram bot token
        """
        return self.__token__

    def get_secret(self):
        """
            Get and config a unique id for the bot
            :return: unique key value - generated previously
        """
        return self.__secret__
