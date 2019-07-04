from bs4 import BeautifulSoup
from collections import Counter
import json


def parse_datafile(filename):

    with open(filename, 'r') as fn:
        s = json.load(fn)
        #soup = BeautifulSoup(fn.read(), features='lxml')
        print(s['html'])

    tag_words = []
"""
    articles = soup.find_all('article', limit=105)

    for article in articles:
        if article.find('script'):
            continue

        story_tags = article.find('div', {'class': 'story__tags tags'})
        tags = story_tags.find_all('a', {'class': 'tags__tag'})
        for tag in tags:
            word = tag.get('data-tag')
            if word is not None:
                tag_words.append(word)

    return Counter(tag_words).most_common(10)
"""

print(parse_datafile('page.html'))

