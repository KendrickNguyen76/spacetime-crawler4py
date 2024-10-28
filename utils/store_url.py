import os
import re
from urllib.parse import urlparse
import hashlib
import zipfile
import base64
import json 

mappings_file = "url_mappings.json"
# Load existing mappings from the file, or create a new dictionary if the file doesn't exist
if os.path.exists(mappings_file) and os.path.getsize(mappings_file) > 0:
    with open(mappings_file, "r") as f:
        url_mappings = json.load(f)
else:
    url_mappings = {}

def store_url_content(resp):
    url = resp.raw_response.url
    content = resp.raw_response.content

    folder_path = get_domain_path(url)
    os.makedirs(folder_path, exist_ok=True)

    # Avoid special characters like '&', '/', '?' in urls that mean smt different in file paths
    url_encoded = base64.urlsafe_b64encode(url.encode()).decode()
    zip_filename = os.path.join(folder_path, f"{url_encoded}.zip")

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(f"{url_encoded}.txt", content.decode('utf-8', errors='ignore'))

    return []

def get_domain_path(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname

    # Split hostname into parts
    host_parts = host.split('.')

    if len(host_parts) >= 2 and host_parts[-2] == 'uci' and host_parts[-1] == 'edu':
        base_domain = '.'.join(host_parts[-2:])  # "uci.edu"
        
        if len(host_parts) > 2:
            subdomain_parts = host_parts[:-2]
            if subdomain_parts[0] == "www":
                subdomain_parts = subdomain_parts[1:]  # Remove "www"
            subdomain = '/'.join(subdomain_parts)
        else:
            subdomain = 'www'
    else:
        base_domain = '.'.join(host_parts[-2:])
        if len(host_parts) > 2:
            subdomain_parts = host_parts[:-2]
            if subdomain_parts[0] == "www":
                subdomain_parts = subdomain_parts[1:]  # Remove "www"
            subdomain = '/'.join(subdomain_parts)
        else:
            subdomain = 'www'

    # Generate a short hash for the path to keep the filename short
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:10]  # Shorten hash to 10 characters

    # Store the mapping for later retrieval
    url_mappings[url_hash] = url
    with open(mappings_file, "w") as f:
        json.dump(url_mappings, f)

    # Return the shortened path
    folder_path = os.path.join(base_domain, subdomain, url_hash)
    return folder_path

def get_original_url(url_hash):
    # Load mappings from the file
    with open(mappings_file, "r") as f:
        url_mappings = json.load(f)
    
    # Retrieve the original URL using the hash
    return url_mappings.get(url_hash, "URL not found")

def compress(resp):
    url = resp.raw_response.url
    content = resp.raw_response.content
    return 
