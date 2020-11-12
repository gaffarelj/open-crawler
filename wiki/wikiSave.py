import os.path
import mysql.connector
import time
import sys
from threading import Thread

try:
	inst = str(sys.argv[2])
except:
	inst = "1"

#try:
#	worker = str(sys.argv[1])
#except:
#	worker = "1"
#saveExtracts = "C:/openCrawl/" + inst + "/wiki/extracts/" + worker + "/"
saveExtracts = "C:/openCrawl/" + inst + "/wiki/extracts/"

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database='wikipedia'
)

savedLinks = False
savedWords = False

def n_files():
	path, dirs, files = os.walk(saveExtracts).__next__()
	return len(files)

def new_title():
	os.chdir(saveExtracts)
	files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
	return files[0]

def save_links(links):
	global savedLinks
	cursorSaveLink = db.cursor()
	linksS = "('" + ("'), ('").join(l.replace("'", "\'") for l in links)[:-4]
	saveLinks = "INSERT IGNORE INTO urls (title) VALUES " + linksS 
	cursorSaveLink.execute(saveLinks)
	savedLinks = True

def save_words(words, occurences):
	global savedWords
	cursorIncrOccurence = db.cursor()
	cursorSaveWords = db.cursor()
	param0 = list(zip(occurences, words))
	param = list(zip(words, occurences))
	incrOccurence = "UPDATE IGNORE words SET occurence = occurence + %s WHERE word = %s"
	saveWords = "INSERT IGNORE INTO words(word, occurence) VALUES (%s, %s)"
	cursorIncrOccurence.executemany(incrOccurence, param0)
	cursorSaveWords.executemany(saveWords, param)
	savedWords = True
	
while True:
	if n_files() != 0:
		savedLinks = True
		savedWords = True
		title = new_title()
		#print(title + ": ", end='')
		#content = open(saveExtracts + title, "r", encoding="utf8").read().split('@')
		with open(saveExtracts + title, "r", encoding="utf8") as code:
			content = code.read().split('@')
		links = list()
		words = list()
		try:
			links = content[0].split('~')
		except:
			pass
		try:
			words = content[1].split('~')
		except:
			pass
		if len(links) > 1:
			savedLinks = False
			Thread(target = save_links(links)).start()
			#save_links(links)
		wordsT = list()
		occurenceT = list()
		for word in words[:-1]:
			wordsT.append(word.split("-")[0])
			occurenceT.append(word.split("-")[1])
		if len(wordsT) > 1:
			savedWords = False
			Thread(target = save_words(wordsT, occurenceT)).start()
			#save_words(wordsT, occurenceT)
		
		while not (savedWords and savedLinks):
			time.sleep(0.02)
		saved = False
		while not saved:
			try:
				os.remove(saveExtracts + title)
				saved = True
			except:
				time.sleep(0.05)
				saved = False
		#print("saved")
	else:
		time.sleep(0.2)