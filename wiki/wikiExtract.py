import os.path
import re
import unidecode
import time
import sys
from bs4 import BeautifulSoup
from threading import Thread

try:
	inst = str(sys.argv[2])
except:
	inst = "1"

savePath = "C:/openCrawl/" + inst + "/wiki/pages/"
saveExtracts = "C:/openCrawl/" + inst + "/wiki/extracts/"
#sw = 1

doneLinks = False
doneWords = False
linksST = ""
wordsST = ""

def n_files():
	path, dirs, files = os.walk(savePath).__next__()
	return len(files)

def new_title():
	os.chdir(savePath)
	files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
	return files[0]

def clean_link(a):
	link = a.get("href")
	if link is None:
		return link
	linkMatch = re.search('^\/wiki\/([a-zA-Z0-9_()\-%]+)$', link)
	if linkMatch:
		return linkMatch.group(1)
	else:
		return None

def clean_text(txt):
	txt = unidecode.unidecode(txt)
	txt = txt.lower()
	txt = re.sub('[^0-9a-zA-Z]+', ' ', txt)
	return txt

def get_links(html):
	global linksST
	global doneLinks
	links = list()
	for a in html.find_all('a'):
		link = clean_link(a)
		if link is not None and link not in links:
			links.append(link)
	for link in links:
		linksST += link + "~"
	#print(str(len(links)) + "L - ", end='')
	doneLinks = True

def get_words(html):
	global wordsST
	global doneWords
	words = dict()
	for bodyText in html.find_all("div", {"id": "mw-content-text"}):
		for p in bodyText.find_all("p"):
			txt = clean_text(p.text)
			wordsT = txt.split(' ')
			for wordT in wordsT:
				if wordT != "":
					if wordT in words:
						words[wordT] += 1
					else:
						words[wordT] = 1
	for word in words.keys():
		wordsST += word + "-" + str(words[word]) + "~"
	#print(str(len(words)) + "W")
	doneWords = True

while True:
	if n_files() != 0:
		title = new_title()
		#print(title + ": ", end='')
		with open(savePath + title, "r", encoding="utf8") as code:
			html = code.read()
		parsed = BeautifulSoup(html, features="html.parser")
		body = parsed.find("div", {"id": "bodyContent"})

		doneLinks = False
		doneWords = False
		linksST = ""
		wordsST = ""
		Thread(target = get_links(body)).start()
		Thread(target = get_words(body)).start()

		while not (doneLinks and doneWords):
			time.sleep(0.05)
		save = linksST + "@" + wordsST

		with open(saveExtracts + title, "wb") as code:
			code.write(save.encode())

		saved = False
		while not saved:
			try:
				os.remove(savePath + title)
				saved = True
			except:
				time.sleep(0.02)
				saved = False
	else:
		time.sleep(0.2)