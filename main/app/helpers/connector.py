import requests
from logging import info, warning, getLogger, INFO


def get_article_response(name):
    getLogger().setLevel(level=INFO)
    tries = 0
    while tries < 11:
        try:
            with requests.Session() as sess:
                with sess.get(url="https://en.wikipedia.org/wiki/?search={name}".format(name=name)) as res:
                    if res.status_code == 200 and res.reason == 'OK':
                        info("Article retrieved: '{}' with a time of: {}".format(name.replace("+", " "), res.elapsed))
                        return res
                    elif res.status_code == 404:
                        return res
                    else:
                        warning("Failed to retrieve Wikipedia article - Status: {code} Reason: {msg}".format(code=res.status_code, msg=res.reason))
        except requests.exceptions.ConnectionError:
            warning("Check your internet connection - Attempt #{} to get response".format(tries))
            tries += 1