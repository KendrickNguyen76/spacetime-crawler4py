# tokenizer.py

"""
Code taken from the Part A of assignment 1. Will be reused for determining
the longest web page.
"""

# tokenize_line
# Needs to be given a string representing a line of text from a file.
# Iterates through the line of text, and converts it into a series of tokens.
# Tokens are defined as a sequence of english, alphanumeric characters
def tokenize_line(line_of_text : str) -> list[str]:
    line_of_text += "\n"
    curr_word = ""
    words = []

    for i in range(len(line_of_text)):
        code = ord(line_of_text[i].lower())

        if (48 <= code <= 57 or 97 <= code <= 122):
            curr_word += chr(code)
        else:
            if len(curr_word) > 0:
                words.append(curr_word)
                curr_word = ""

    return words


# tokenize
# Needs to be given a file path. Converts all of the text of that file into
# a list of tokens.
def tokenize(file_path : str) -> list[str]:
    all_tokens = []

    with open(file_path) as word_file:
        for line in word_file:
            all_tokens += tokenize_line(line)

    return all_tokens


# compute_word_frequencies
# Needs to be given a list of tokens. Records the frequency of each
# token within a dictionary and then returns it.
def compute_word_frequencies(token_list : list[str]) -> dict[str, int]:
    word_frequencies = dict()

    for token in token_list:
        if token not in word_frequencies:
            word_frequencies[token] = 1
        else:
            word_frequencies[token] += 1

    return word_frequencies