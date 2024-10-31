# top_fifty_dict.py

"""
Code for TopFiftyDict, a class that will store all of the tokens from
our HTML files and also help pick the 50 most common ones
"""

class TopFiftyDict:
    # CONSTANTS
    MAX_LENGTH = 50

    # Initialized the object w/ one instance variable,
    # self._token_dict
    def __init__(self):
        self.__token_dict = dict()

    # Sorts self._token_dict and cuts it down to the first 50 items
    def __sort_dict(self):
        self.__token_dict = dict(sorted(self.__token_dict.items(), 
                                key = lambda tup: tup[1], 
                                reverse = True))
        self.__token_dict = dict(list(self.__token_dict.items())[:50])

    # Takes in a list of strings which represent tokens.
    # Adds them to self._token_dict
    def add_to_dict(self, token_list : list[str]) -> None:
        for token in token_list:
            if token not in self.__token_dict:
                self.__token_dict[token] = 1
            else:
                self.__token_dict[token] += 1
        
        self.__sort_dict()

    def print_fifty_word_dict()
    
    # Handles string representation of a TopFiftyDict
    def __str__(self):
        return str(self.__token_dict)
    
