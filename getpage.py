#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
import re
from urllib.parse import unquote
from string import punctuation


# Si vous écrivez des fonctions en plus, faites-le ici
global cache
cache = {}

def getJSON(page):

    params = urlencode({
      'format': 'json',  # TODO: compléter ceci
      'action': 'parse',  # TODO: compléter ceci
      'prop': 'text',
      'redirects': True,
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"
    response = urlopen(API + "?" + params)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    if(page in cache.keys()):
        return cache[page]
    title, content = getRawPage(page)
    try:
        soup = BeautifulSoup(content, 'html.parser')
        links = []
        for div in soup.find_all('div'):
            for p in div.find_all('p', recursive = False):
                for a in p.find_all('a', href = True):
                    # Check if link is valid format
                    if(re.match("/wiki/", a['href'])):
                        lnk = unquote((a['href'].split('/wiki/')[1]))
                        lnk_to_display = lnk.split("#")[0]
                        lnk_to_display = lnk_to_display.replace('_', ' ')
                        if(any(p in lnk_to_display for p in ':,.+=?!*')):
                            pass
                        else:
                            links.append((lnk, lnk_to_display))
            seen = set()
            links = [x for x in links if not (x[1] in seen or seen.add(x[1]))]
        cache[page] = title, links[:10] #, links_to_display[:10]]
        return unquote(title), links[:10] #, links_to_display[:10]]
    except TypeError:
        print('La page est surement invalide...')
        return None, []


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    #print("Ça fonctionne !")
    #print(getJSON("Utilisateur:A3nm/INF344"))
    #a = getJSON("Utilisateur:A3nm/INF344")
    #print(loads(a)['parse']['title'])
    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    #print('AAAAAAA')
    #print(a)
    print(getPage("Utilisateur:A3nm/INF344"))
    #print('BBBBBBBBBBBB')
    #print(b)
    # print(getRawPage("Histoire"))
