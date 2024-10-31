# top_fifty.py

"""
Code for python script that will run through all of our collected HTML files
and return the top 50 most common words
"""

# Imports
from utils import tokenizer, extract_text
import os
from pathlib import Path

# Constants
# File path for full folder, we're going to assume it's always in the same place
HTML_ZIP_DIRECTORY = Path("uci.edu")  
# File path for a subdirectory within uci.edu that will be used for testing
TEST_FILES_DIRECTORY = Path("uci.edu/accessibility/ics")

# get_top_fifty_words()
# Needs to be given a path to the directory that contains all of 
# the HTML zip files. Goes through all of them and find the top
# 50 words.
def get_top_fifty_words(file_path : Path):
    # Walks through the directories and subdirectories of file_path
    for root, dir, files in os.walk(file_path):
        for file in files:
            if file.endswith(".zip"):
                # Creates a path for the zip_file
                zip_path = Path(root, file)
                print(zip_path)
                    

# Main
# Gets called when script is run
if __name__ == "__main__":
    get_top_fifty_words(TEST_FILES_DIRECTORY)
