# tokenizer.py

"""
Code taken from the Part A of assignment 1. Some parts will be reused for determining
the longest web page.
"""

# Stop Words set
STOP_WORDS = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}
VALID_CHARS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}


# tokenize_line()
# Needs to be given a string representing a line of text from a file.
# Iterates through the line of text, and converts it into a series of tokens.
# Tokens are defined as a sequence of english, alphanumeric characters
def tokenize_line(line_of_text : str) -> list[str]:
    line_of_text += "\n"
    curr_word = ""
    words = []
    
    for i in range(len(line_of_text)):
        char = line_of_text[i].lower()

        if char in VALID_CHARS:
            curr_word += char
        else:
            # Changed the minimum length of curr_word to be 2 instead of 1
            # this is to avoid accidentally picking up on too many random 
            # singular letters
            if (curr_word not in STOP_WORDS) and len(curr_word) > 2:
                words.append(curr_word)

            curr_word = ""

    return words


# tokenize()
# Needs to be given a list of strings. Converts the list of strings into
# a list of tokens.
def tokenize(text_list : list[str]) -> list[str]:
    all_tokens = []

    for single_text in text_list:
        #print(single_text)
        all_tokens += tokenize_line(single_text)

    return all_tokens


# compute_word_frequencies()
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