import os.path
import subprocess
import time
import mysql.connector
import requests

time.sleep(30)
instances = 5#int(input("Number of instances: "))

basDir = "C:/openCrawl/"
#directories = ["/wiki/", "/wiki/extracts/", "/wiki/extracts/1/",
#"/wiki/extracts/2/", "/wiki/pages/"]
directories = ["/wiki/", "/wiki/extracts/", "/wiki/extracts/", "/wiki/pages/"]
for directory in directories:
	for i in range(1, instances + 1):
		if not os.path.exists(basDir + str(i) + directory):
			os.makedirs(basDir + str(i) + directory)

#scripts = ["wikiDown.py 1", "wikiExtract.py 1", "wikiSave.py 1", "wikiSave.py
#2"]
scripts = ["wikiDown.py 1", "wikiExtract.py 1", "wikiSave.py 1"]
for script in scripts:
	for i in range(1, instances + 1):
		subprocess.Popen("python ../../" + script[:-4] + "/" + script[:-4] + "/" + script + " " + str(i))

db = mysql.connector.connect(host="localhost",
  user="root",
  passwd="",
  database='wikipedia')

cursor = db.cursor()
totalWords = "SELECT COUNT(*) FROM words"
totalUrls = "SELECT COUNT(*) FROM urls"
visitedUrls = "SELECT COUNT(*) FROM urls WHERE visited = 1"
initVisited = "UPDATE urls SET to_visit = 0 WHERE visited = 0 and to_visit != 0"
#cursor.execute(initVisited)
interval = 2.5#float(input("Interval between stats (in min): "))
cursor.execute(totalWords)
rslt = cursor.fetchall()
nWords0 = int(rslt[0][0])
cursor.execute(totalUrls)
rslt = cursor.fetchall()
nUrls0 = int(rslt[0][0])
cursor.execute(visitedUrls)
rslt = cursor.fetchall()
nVisited0 = int(rslt[0][0])
t = 0
while True:
	cursor.execute(totalWords)
	rslt = cursor.fetchall()
	nWords1 = rslt[0][0]
	cursor.execute(totalUrls)
	rslt = cursor.fetchall()
	nUrls1 = rslt[0][0]
	cursor.execute(visitedUrls)
	rslt = cursor.fetchall()
	nVisited1 = rslt[0][0]
	toPrint = str(round(t * interval, 1)) + " - "
	toPrint += "{:,}".format(nWords1) + " W  on  " + "{:,}".format(nVisited1) + " V  of  " + "{:,}".format(nUrls1) + " U  (" + str(round(nVisited1 / nUrls1 * 100, 2)) + "%)\t – \t"
	toPrint += str(round((nWords1 - nWords0) / (interval*60), 1)) + " W/s ; " + str(round((nUrls1 - nUrls0) / (interval*60), 1)) + " U/s ; " + str(round((nVisited1 - nVisited0) / (interval*60), 1)) + " V/s"
	print(toPrint)
	requests.get("https://renseign.com/private/wikiCrawl?stats=" + toPrint)
	nWords0, nUrls0, nVisited0 = nWords1, nUrls1, nVisited1
	time.sleep(interval*60)
	t += 1