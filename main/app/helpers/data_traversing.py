from bs4 import element as ele
from logging import info, getLogger, INFO


def get_first_disambiguous_page(element):
    import main.app.core.wiki_scraper as wk

    getLogger().setLevel(level=INFO)
    hyperlink = get_next_tag(curr=element, sameFamily=False, tag='a')
    if hyperlink.has_attr("href"):
        link = hyperlink.get("href", "")
        if link.startswith('/wiki/') and not ":" in link:
            link = link.replace("/wiki/", "")
            info("Redirecting to Wikipedia page: '{}'...".format(link))
            return wk.wiki_scraper(link)
        else:
            return get_first_disambiguous_page(hyperlink)
    else:
        return get_first_disambiguous_page(hyperlink)


def get_article_content(soup, name):

    content = soup.find(name='div',
                        attrs={"id": "content", "class": "mw-body", "role": "main"})
    assert content is not None, "No main content"

    content = get_child(curr=content, tag='div',
                        attrs={'id': 'bodyContent', 'class': ['mw-body-content']})
    assert content is not None, "No body content"

    content = get_child(curr=content,
                        tag='div',
                        attrs={'id': 'mw-content-text', 'lang': 'en', "dir": "ltr", 'class': ['mw-content-ltr']})
    assert content is not None, "Failed to verify body content text - Article: '{}' may not exist!".format(name)

    content = get_child(curr=content,
                        tag='div',
                        attrs={'class': ['mw-parser-output']})
    assert content is not None, "No parser output"

    return content


def get_next_tag(curr, tag, sameFamily, attrs=None):
    if sameFamily:
        curr = curr.next_sibling
    else:
        curr = curr.next

    assert curr is not None, "No next element"
    if attrs is not None:
        if isinstance(curr, ele.Tag) and curr.name == tag and curr.attrs == attrs:
            return curr
        else:
            return get_next_tag(curr=curr, tag=tag, sameFamily=sameFamily, attrs=attrs)
    else:
        if isinstance(curr, ele.Tag) and curr.name == tag:
            return curr
        else:
            return get_next_tag(curr=curr, tag=tag, sameFamily=sameFamily, attrs=attrs)
        

def get_child(curr, tag, attrs=None, text=None):
    for child in curr:
        if attrs is not None:
            if text is not None:
                if isinstance(child, ele.Tag) and child.name == tag and child.attrs == attrs and child.text==text:
                    return child
            else:
                if isinstance(child, ele.Tag) and child.name == tag and child.attrs == attrs:
                    return child
        elif text is not None:
            if isinstance(child, ele.Tag) and child.name == tag and child.text == text:
                return child
        else:
            if isinstance(child, ele.Tag) and child.name == tag:
                return child
