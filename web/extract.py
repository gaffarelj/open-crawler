import os.path
import re
import unidecode
import time
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

tags = [["h1", 1.4], ["h2", 1.3], ["h3", 1.2], ["h4", 1.1], ["h5", 1], ["h6", 0.6], ["b", 1], ["em", 0.8], ["i", 0.8], ["u", 0.9], ["mark", 1.1], ["strong", 1], ["ins", 0.9], ["cite", 0.9], ["small", 0.5], ["del", 0.4], ["p", 0.7]]

def clean_link(a, url):
	link = a.get("href")
	if link is None:
		return link
	link = urljoin(url, link)
	linkMatch = link[:6] + re.findall("^[^#':!]+", link[6:])[0]
	if linkMatch is not None:
		if linkMatch[-1:] == '/':
			return linkMatch[:-1]
		return linkMatch
	else:
		return None

def clean_text(txt):
	txt = unidecode.unidecode(txt)
	txt = txt.lower().replace("\n", "").replace("\t", "")
	txt = re.sub('[^0-9a-zA-Z]+', ' ', txt)
	return txt

def get_links(html, url):
	global prnt
	links = list()
	try:
		for a in html.find_all('a'):
			link = clean_link(a, url)
			if link is not None and link not in links:
				links.append(link)
	except:
		pass
	return links

def get_words(html):
	global prnt
	words = dict()
	rslt = ""
	for tagV in tags:
		tag = tagV[0]
		weight = tagV[1]
		try:
			for element in html.find_all(tag):
				txt = clean_text(element.text)
				wordsT = txt.split(' ')
				for wordT in wordsT:
					if wordT != "":
						if wordT in words:
							words[wordT] += weight
						else:
							words[wordT] = weight
		except:
			pass
	try:
		maxW = max(words.values())
	except:
		maxW = 10
	words.update((x, y*5/maxW) for x, y in words.items())
	return words

def extract(html, url):
	parsed = BeautifulSoup(html, features="html.parser")
	links = get_links(parsed, url)
	words = get_words(parsed)
	return links, words
