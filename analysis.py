import os
import zipfile
import json
from utils import tokenizer, extract_text
from urllib.parse import urlparse, urlunparse
from collections import defaultdict

# Function to search through directories and find zip files
def analysis(directory, url_mapping):
    longest_page = None
    longest_length = 0
    urls = set()
    subdomains = defaultdict(set)

    # Open analysis.txt for writing output
    with open("analysis.txt", "w") as output_file:
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
                                    subdomain, stripped_url = url_extract(url)
                                    urls.add(stripped_url)
                                    if subdomain:
                                        subdomains[subdomain].add(stripped_url)
                                    # Read the content of the text file
                                    with zip_ref.open(zip_info.filename) as text_file:
                                        html_content = text_file.read().decode("utf-8")
                                        
                                        # Write the URL and HTML content to analysis.txt
                                        output_file.write(f"URL: {stripped_url}\n")
                                        tokens = tokenizer.tokenize(extract_text.extract_text(html_content))
                                        if len(tokens) > longest_length:
                                            longest_page = stripped_url
                                            longest_length = len(tokens)
                                else:
                                    output_file.write(f"No URL found for encrypted string: {encrypted_string}\n")
        
        # Write subdomain analysis to analysis.txt
        output_file.write("Subdomains and their URL counts:\n")
        for subdomain in sorted(subdomains.keys()):
            output_file.write(f"{subdomain}, {len(subdomains[subdomain])}\n")
        
        output_file.write(f"Total number of URLs: {len(urls)}\n")
        output_file.write(f"Longest page: {longest_page} with {longest_length} tokens\n")

def url_extract(url):
    parsed_url = urlparse(url)
    stripped_url = urlunparse(parsed_url._replace(fragment=""))
    subdomain = None
    hostname = parsed_url.hostname
    if not hostname:
        return (subdomain, stripped_url)
    parts = hostname.split('.')
    if len(parts) > 2 and parts[-2] == "uci" and parts[-1] == "edu":
        subdomain = '.'.join(parts[:-2])
    return (subdomain, stripped_url)

if __name__ == "__main__":
    # Define the main directory and JSON mapping filename
    main_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uci.edu")  # Assumes script is in the same location
    json_mapping_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "url_mappings.json")

    # Load the JSON mapping file
    with open(json_mapping_file, "r") as f:
        url_mapping = json.load(f)
    analysis(main_directory, url_mapping)
