from bs4 import BeautifulSoup
import re


def extract_text(html_text):
    # Parse the HTML
    soup = BeautifulSoup(html_text, "html.parser")

    # Extract keywords from meta tags and title
    keywords = []
    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description:
        keywords.append(meta_description["content"])

    title = soup.find("title")
    if title:
        keywords.append(title.get_text())

    # Extract visible text elements
    visible_texts = []
    for element in soup.find_all(text=True):
        if element.parent.name not in ["script", "style", "noscript", "meta", "link", "head"]:
            text = element.strip()
            if text:
                visible_texts.append(text)

    # Combine keywords and visible text, then print or use further
    all_keywords = keywords + visible_texts
    return all_keywords