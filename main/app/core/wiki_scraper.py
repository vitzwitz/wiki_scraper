"""
Instructions:
    1. Write a python module that correctly satisfies the specs in the test_wiki_scraper.py module
    2. Write a bash script that executes the tests and exports the test results to an xunit file
    3. Employ as many best practices as you find appropriate

To get started:
    1. Install nose from the requirements.txt file using 'pip install -r requirements.txt'
    2. Run the unit tests by running 'nosetests' from inside the 'wiki_scraper' path

Good luck!
"""


from logging import warning, getLogger, INFO
from bs4 import BeautifulSoup as bs, element as ele
from main.app.helpers import data_manipulator as dm, connector as cn, data_traversing as dt


def get_links(paragraph, name, def_ambig):

    contains_name = [False, None]
    if dm.redirect(paragraph.text) or (def_ambig and name in paragraph.text):
        return dt.get_first_disambiguous_page(paragraph)
    definition = None
    links = []
    for child in paragraph:
        if isinstance(child, ele.Tag):
            if child.name == 'b' and not contains_name[0]:
                if '(' in name and ')' in name and not contains_name[0]:
                    s = name.index('(')
                    f = name.index(')')
                    definition = name[s + 1:f]
                    contains_name = [dm.has_name(text=child.text, title=name[:s-1]), False]
                elif ',' in name and not contains_name[0]:
                    c = name.index(',')
                    has_all_words = True
                    for word in name[c:].split(','):
                        if not word.lower() in paragraph.text.lower():
                            has_all_words = False

                    contains_name = [dm.has_name(text=child.text, title=name[:c]), has_all_words]
                elif not contains_name[0]:
                    contains_name = [dm.has_name(text=child.text, title=name), None]

            if child.name == 'a' and child.has_attr("href"):
                if links == [] and definition is not None and contains_name[1] is not None and not contains_name[1]:
                    contains_name[1] = definition in child.text
                links = collect_links(child=child, links=links)

    if (not contains_name[0] or (definition is not None and not contains_name[1])) and \
            not name.lower() in paragraph.text.lower():
        paragraph = dt.get_next_tag(curr=paragraph, sameFamily=True, tag='p')
        return get_links(paragraph=paragraph, name=name, def_ambig=def_ambig)
    if not links:
        warning("No content links found in paragraph: {}".format(name))
    return links


def collect_links(child, links):
    path = child.get("href", "")
    if path.startswith('/wiki/'):
        path = path.replace("/wiki/", "")
        if not ":" in path:
            if not "https://en.wikipedia.org/wiki/{path}".format(path=path) in links:
                links.append("https://en.wikipedia.org/wiki/{path}".format(path=path))
    return links


def wiki_scraper(name):
    getLogger().setLevel(level=INFO)
    resp = cn.get_article_response(dm.get_proper_article_name(name=name))
    assert resp is not None, "Failed to get response"
    if resp.status_code == 404:
        warning("There is no article for '{}'".format(name))
        return []

    article = resp.text
    soup = bs(markup=article, features="html.parser")

    title = soup.title.text.replace(" - Wikipedia", "")
    content = dt.get_article_content(soup=soup, name=name)

    def_ambig = "(disambiguation)" in title
    if def_ambig:
        title = title.replace(' (disambiguation)', '')

    content = dt.get_child(content, 'p', attrs={})
    if content is None:
        raise AssertionError('Failed to find a paragraph in the content of the page: {} - Possibly illegal wikipedia page'
                             .format(title))

    while content.text is None and content.text.strip() == "":
        content = dt.get_child(curr=content, tag='p')

    assert content is not None, "No paragraphs in the body"
    return get_links(paragraph=content, name=title, def_ambig=def_ambig)
