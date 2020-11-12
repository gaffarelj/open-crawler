import requests
import os.path
import time
import mysql.connector
import sys

try:
	inst = str(sys.argv[2])
except:
	inst = "1"

titles = dict()
i_title = 0

savePath = "C:/openCrawl/" + inst + "/wiki/pages/"
n_max = 25

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database='wikipedia'
)

def n_files():
	path, dirs, files = os.walk(savePath).__next__()
	return len(files)

def get_titles():
	cursorReserveTitle = db.cursor(prepared=True)
	cursorGetTitle = db.cursor(prepared=True)
	reserveTitle = "UPDATE urls SET to_visit = " + inst + " WHERE visited = 0 and to_visit = 0 LIMIT 50"
	getTitle = "SELECT title FROM urls WHERE to_visit = " + inst
	i = 0
	while i == 0:
		cursorReserveTitle.execute(reserveTitle)
		cursorGetTitle.execute(getTitle)
		rslt = cursorGetTitle.fetchall()
		for titleT in rslt:
			titles[i] = titleT[0].decode()
			i += 1
		if i == 0:
			time.sleep(0.2)

def new_title():
	global i_title
	if i_title not in titles:
		get_titles()
		i_title = 0
	title = titles[i_title]
	del titles[i_title]
	i_title += 1
	return title

def title_done(title):
	cursorTitleDone = db.cursor()
	titleDone = "UPDATE urls SET to_visit = 0, visited = 1, last_visit = NOW() WHERE title = '" + title + "'"
	cursorTitleDone.execute(titleDone)

wikiApiBase = "https://en.wikipedia.org/wiki/"

while True:
	if n_files() > n_max - 1:
		time.sleep(0.2)
	else:
		title = new_title()
		gotcha = False
		while not gotcha:
			try:
				req = requests.get(wikiApiBase + title)
				#print(title)
				if req.content is not None:
					with open(savePath + title, "wb") as code:
						code.write(req.content)
					title_done(title)
					gotcha = True
			except:
				time.sleep(1)
				gotcha = False