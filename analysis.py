import os
import zipfile
import json
from utils import tokenizer, extract_text


# Function to search through directories and find zip files
def analysis(directory, url_mapping):
    longest_page = None
    longest_length = 0
    # Traverse the directory and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".zip"):
                zip_path = os.path.join(root, file)
                
                # Open the zip file and extract the text file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for zip_info in zip_ref.infolist():
                        # Check if the file is a text file
                        if zip_info.filename.endswith(".txt"):
                            # Extract the encrypted string (without '.txt')
                            encrypted_string = os.path.splitext(os.path.basename(zip_info.filename))[0]
                            
                            # Match the encrypted string to the URL in JSON mapping
                            url = url_mapping.get(encrypted_string)
                            if url:
                                # Read the content of the text file
                                with zip_ref.open(zip_info.filename) as text_file:
                                    html_content = text_file.read().decode("utf-8")
                                    
                                    # Print the URL and HTML content
                                    print(f"URL: {url}")
                                    tokens = tokenizer.tokenize(extract_text.extract_text(html_content))
                                    if len(tokens) > longest_length:
                                        longest_page = url
                                        longest_length = len(tokens)
                                    print(f"Tokens: {tokens}")
                                    # print(f"HTML Content:\n{html_content}\n{'-'*40}\n")
                                    # print(tokenizer.tokenize(text_file))
                            else:
                                print(f"No URL found for encrypted string: {encrypted_string}")
    print(f"Longest page: {longest_page} with {longest_length} tokens")


if __name__ == "__main__":
    # Define the main directory and JSON mapping filename
    main_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uci.edu")  # Assumes script is in the same location
    json_mapping_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "url_mappings.json")

    # Load the JSON mapping file
    with open(json_mapping_file, "r") as f:
        url_mapping = json.load(f)
    analysis(main_directory, url_mapping)
    # parser = ArgumentParser()
    # parser.add_argument("--restart", action="store_true", default=False)
    # parser.add_argument("--config_file", type=str, default="config.ini")
    # args = parser.parse_args()
    # main(args.config_file, args.restart)