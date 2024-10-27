import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from utils.store_url import store_url_content
from utils.is_valid_checks import infinite_trap, is_large_file
def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    if not resp.status == 200 or infinite_trap(resp) or is_large_file(resp):
        print(f"The following actual url {resp.url} had error code {resp.error}.\nReached via url: {url}")
        return list()
    # Store current url and resp if it is valid (status 200)
    store_url_content(resp)

    urls = set()
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    for link in soup.find_all('a'):
        url = link.get('href')
        parsed = urlparse(url)
        removed_fragment = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ''))
        urls.add(removed_fragment)
    return list(urls)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        ics_domains = [
            r".*\.ics\.uci\.edu",
            r".*\.cs\.uci\.edu",
            r".*\.informatics\.uci\.edu",
            r".*\.stat\.uci\.edu",
            r"today\.uci\.edu/department/information_computer_sciences"
        ]
        domain_match = any(re.match(domain, parsed.netloc) for domain in ics_domains)
        if not domain_match:
            return False
        parsed_path = parsed.path.lower()
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|heic)$", parsed_path):
            return False
        calendar_urls = [
            "wics-meeting-dbh-5011",
            "events/tag/talk/day",
            "events/tag/talk",
            "events/category/info-session/day"
        ]
        for calendar_url in calendar_urls:
            if calendar_url in parsed_path:
                return False
        
        query_urls = [
            r"action=download&upname=",
            r"action=upload&upname=",
            r"action=login",
            r"action=edit",
            r"action=refcount",
            r"action=crypt",
            r"action=search&q",
            r"tribe-bar-date=",
            r"share=",
            r"outlook-ical=",
            r"ical=",
            r"redirect_to="
        ]
        query_match = any(re.search(query, parsed.query) for query in query_urls)
        if query_match:
            return False
        
        date_pattern = r'/(\d{4}([-/]\d{2}([-/]\d{2})?)?|(\d{2}([-/]\d{4})))$'
        if bool(re.search(date_pattern, parsed_path)):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|heic)$", parsed.query.lower())
        
    except TypeError:
        print ("TypeError for ", parsed)
        raise