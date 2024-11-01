# top_fifty.py

"""
Code for python script that will run through all of our collected HTML files
and return the top 50 most common words
"""

# Imports
from utils import tokenizer, extract_text, top_fifty_dict
import os
import zipfile
from pathlib import Path

# Constants
# File path for full folder, we're going to assume it's always in the same place
HTML_ZIP_DIRECTORY = Path("uci.edu")  
# File path for a subdirectory within uci.edu that will be used for testing
TEST_FILES_DIRECTORY = Path("uci.edu/accessibility/ics")


# process_zip_file_text()
# Needs to be given a path to a zip_file. Processes it by turning
# its contents into tokens that can be used for analysis
def process_zip_file_text(zip_file_path : Path):
    # First, open the zip_file_path as a ZipFile object
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Get the names of all the files in the zip
        for file_name in zip_ref.namelist():
            # Now actually open up the files
            with zip_ref.open(file_name) as text_file:
                # Turn the text in each file into tokens
                html_content = text_file.read().decode("utf-8")
                return tokenizer.tokenize(extract_text.extract_text(html_content))


# get_top_fifty_words()
# Needs to be given a path to the directory that contains all of 
# the HTML zip files. Goes through all of them and find the top
# 50 words.
def get_top_fifty_words(file_path : Path):
    total_word_frequency = top_fifty_dict.TopFiftyDict()

    # Walks through the directories and subdirectories of file_path
    for root, dir, files in os.walk(file_path):
        for file in files:
            if file.endswith(".zip"):
                # Creates a path for the zip_file
                zip_path = Path(root, file)
                #print(zip_path)
                # Pass it off to process_zip_file_text() to handle tokenization
                token_list = process_zip_file_text(zip_path)
                total_word_frequency.add_to_dict(token_list)
    
    return total_word_frequency


# Main
# Gets called when script is run
if __name__ == "__main__":
    top_fifty = get_top_fifty_words(TEST_FILES_DIRECTORY)
    top_fifty.print_fifty_word_dict()
