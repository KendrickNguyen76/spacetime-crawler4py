import os
import zipfile
import json
from utils import tokenizer, extract_text
from urllib.parse import urlparse, urlunparse
from collections import defaultdict

# Function to iterate over zip files of site content and report analysis
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
                    z_path = os.path.join(root, file)
                    
                    with zipfile.ZipFile(z_path, 'r') as z_file:
                        for zip_info in z_file.infolist():
                            if zip_info.filename.endswith(".txt"):
                                encrypted_url = os.path.splitext(os.path.basename(zip_info.filename))[0]
                                url = url_mapping.get(encrypted_url)
                                if url:
                                    subdomain, stripped_url = url_extract(url)
                                    urls.add(stripped_url)
                                    if subdomain:
                                        subdomains[subdomain].add(stripped_url)
                                    with z_file.open(zip_info.filename) as text_file:
                                        html_content = text_file.read().decode("utf-8")
                                        
                                        # Write the URL and HTML content to analysis.txt
                                        output_file.write(f"URL: {stripped_url}\n")
                                        tokens = tokenizer.tokenize(extract_text.extract_text(html_content))
                                        if len(tokens) > longest_length:
                                            longest_page = stripped_url
                                            longest_length = len(tokens)
                                else:
                                    output_file.write(f"No URL found for encrypted url: {encrypted_url}\n")
        
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
    # Define the main directory which is where all the zip files of site content are stored
    main_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uci.edu")
    json_mapping_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "url_mappings.json")
    # Mapping file maps encrypted urls to actual urls
    with open(json_mapping_file, "r") as f:
        url_mapping = json.load(f)
    analysis(main_directory, url_mapping)
