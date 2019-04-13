import itertools
import string

import requests
import logging as log
from constants import Constants
""" 
S = requests.Session()

PARAMS = {
    "action": "query",
    "format": "json",
    "generator": "allpages",
    "gtitles":"Luffy",
    "list": "allimages"
}

url = 'https://onepiece.fandom.com/api.php'

print(requests.get(url=url, params=PARAMS).content)
"""

class Fetcher:

    def __init__(self):
        self._imagestartlink = 'https://onepiece.fandom.com/api.php?action=imageserving&format=json&wisTitle='
        self._querystartlink = 'https://onepiece.fandom.com/api.php?format=json&action=query&'
        self.constants = Constants()

    def cleanName(self, name):
        """ignore all special characters, numbers, whitespace, case"""
        return ''.join(c for c in name.lower() if c in string.ascii_lowercase)

    def get_wiki_pages(self, names):
        pages = []
        for name in names:
            pages.append(self.__fetch_page(name))

        return pages

    def __get_correct_page(self, checked_name, all_pages):
        # Gets first page
        first_page = None
        log_string = ""

        clean_name = self.cleanName(checked_name)

        # Checks for any direct hits.
        # difflib.get_close_matches[0]
        for nr, page in enumerate(all_pages.values()):
            title = page['title']
            title_clean = self.cleanName(title)
            log_string += title + ","
            if title_clean == clean_name:
                log.info("Found direct match, page nr {}: {}".format(nr + 1, clean_name))
                first_page = page
                break


        # Get first containing
        # if not first_page:
        #     pages = all_pages.values()
        #     pages_containing = [page for page in pages if checked_name in page['title'].lower()]
        #     if pages_containing:
        #         first_page = pages_containing[0]
        #         print("bingo")

        # Gets first entry
        if not first_page:
            first_page = next(iter(all_pages.values()))

        log.info("Input name: {} \n Parsed titles were: {}.\n Result title was: {}".format(checked_name, log_string[:-1],
                                                                                           first_page["title"]))

        return first_page



    def __fetch_page(self, name):

        # Returns translated name or the same name
        #clean_name = self.cleanName(name)
        checked_name = self.constants.translateAlt(self.cleanName(name))

        if checked_name == self.cleanName(name):
            checked_name = name

        # All pages with "name" in there, and their URLs.
        fetch_json = requests.get(self._querystartlink + '&prop=info&inprop=url&generator=allpages&gapfrom=' + checked_name.title()
                                  ).json() #'Use "gapfilterredir=nonredirects" option instead of "redirects" when using allpages as a generator' #gaplimit=1

        # Gets the first page
        all_pages = fetch_json['query']['pages']

        first_page = self.__get_correct_page(checked_name, all_pages)


        return first_page

        # ASSUME THAT THE FIRST LINK IS CORRECT - MIGHT BE REDIRECTION LINK!



        def check_title(self):
            pass

    def fetch_image_url(self, page):
        pass
        title = str(page["title"])
        image_json = requests.get(self._imagestartlink+title).json()
        return image_json["image"]["imageserving"]


class SpellChecker():
    """Find and fix simple spelling errors.
    based on Peter Norvig
    http://norvig.com/spell-correct.html
    """
    def __init__(self, names):
        self.model = set(names)

    def __known(self, words):
        for w in words:
            if w in self.model:
                return w
        return None

    def __edits(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = (a + b[1:] for a, b in splits if b)
        transposes = (a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1)
        replaces   = (a + c + b[1:] for a, b in splits for c in string.ascii_lowercase if b)
        inserts    = (a + c + b     for a, b in splits for c in string.ascii_lowercase)
        return itertools.chain(deletes, transposes, replaces, inserts)

    def correct(self, word):
        """returns input word or fixed version if found"""
        return self.__known([word]) or self.__known(self.__edits(word)) or word

    """
    # distance 2
    def known_edits2(word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
    """

# Test
#print(requests.get(startlink+'generator=allpages&gapfrom=Luffy&prop=info').content) #prop=info&inprop=url


#image_json = requests.get(startlink+'generator=allpages&gapfrom=Luffy&prop=images').json()
#print(image_json)
#test_output = image_json['query-continue']['']

#All images from the Monkey D. Luffy page
#print(requests.get('https://onepiece.fandom.com/api.php?format=json&action=query&generator=images&titles=Monkey_D._Luffy&prop=imageinfo').content)