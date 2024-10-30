# tokenizer.py

"""
Code taken from the Part A of assignment 1. Some parts will be reused for determining
the longest web page.
"""

# tokenize_line()
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
            if len(curr_word) > 0 and not_stop_word(curr_word):
                words.append(curr_word)
                curr_word = ""

    return words

def not_stop_word(word):
    return word not in {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}


# tokenize()
# Needs to be given a file path. Converts all of the text of that file into
# a list of tokens.
def tokenize(text_file : str) -> list[str]:
    all_tokens = []
    for line in text_file:
        all_tokens += tokenize_line(line)

    return all_tokens