
def get_project_name(name):
    assert name.startswith('Wikipedia:'), 'Not a proper project'
    return name.replace('Wikipedia:', '')


def get_proper_article_name(name):
    if not isinstance(name, str):
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        else:
            raise AssertionError("Invalid Article Name type: Inputted name must be unicode, bytes, or a str")
    if ':' in name:
        raise AssertionError("Invalid page: {} - Name cannot refer to projects, help, etc for Wikipedia"
                             .format(name))
    if "_" in name:
        name = name.replace("_", " ")
    name = "+".join(name.split(" "))
    return name


def has_name(text, title):

    for word in title.split(" "):
        if not word.lower() in text.lower() and word.lower() != text.lower():
            return False
    return True


def redirect(text):

    if " refers to:\n" in text or " refer to:\n" in text or \
            " usually refers to:\n" == text or " may refer to:\n" in text:
        return True
    else:
        return False
