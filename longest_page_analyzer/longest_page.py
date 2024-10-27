# longest_page.py

"""
Code for a program that will take a list of HTML files and figure out which one is
the longest. Goal is count the actual words and ignore any HTMl code.
"""

# Imports
from pathlib import Path
from  bs4 import BeautifulSoup
from tokenizer import tokenize_line


# file_word_counter()
# Takes in a file path to an HTML file, opens it, and then uses BeautifulSoup
# to get the text and count the number of words.
def file_word_counter(file_path : Path) -> int:
    word_count = 0

    with file_path.open() as html_file:
        file_soup = BeautifulSoup(html_file, "html.parser")

        for string in file_soup.stripped_strings:
            # For the sake of simplicity, I'm gonna define a "word" to be a sequence
            # of english alphanumeric characters. I'm not sure if there's a better
            # defintion just yet. 

            words = tokenize_line(string)
            print(words) # for testing
            word_count += len(words)
    
    return word_count


# Main function
def main():
    test_file = Path("test_files/doormouse_story.html")
    count = file_word_counter(test_file)
    print(count) # for testing

if __name__ == "__main__":
    main()