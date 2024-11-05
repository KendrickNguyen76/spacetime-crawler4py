from bs4 import BeautifulSoup


def extract_text(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    # Text is extracted from meta tags and title
    keywords = []
    meta_text= soup.find("meta", attrs={"name": "description"})
    if meta_text:
        keywords.append(meta_text["content"])

    title = soup.find("title")
    if title:
        keywords.append(title.get_text())

    # Text is extracted from visible text
    visible_texts = []
    for element in soup.find_all(text=True):
        if element.parent.name not in ["script", "style", "noscript", "meta", "link", "head"]:
            text = element.strip()
            if text:
                visible_texts.append(text)
    
    all_keywords = keywords + visible_texts
    return all_keywords
