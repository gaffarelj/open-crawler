import requests
import time
import mysql.connector

db = mysql.connector.connect(host="localhost",
  user="root",
  passwd="",
  database='web')

def get_urls(inst_i, limit=150):
	urls = []
	hashes = []
	inst = str(inst_i)
	cursorReserveUrl = db.cursor(prepared=True)
	cursorGetUrl = db.cursor(prepared=True)
	reserveUrl = "UPDATE urls SET to_visit = " + inst + " WHERE visited = 0 and to_visit = 0 LIMIT " + str(limit)
	getUrl = "SELECT url, hash FROM urls WHERE to_visit = " + inst
	i = 0
	while i == 0:
		cursorReserveUrl.execute(reserveUrl)
		cursorGetUrl.execute(getUrl)
		rslt = cursorGetUrl.fetchall()
		for urlT in rslt:
			urls.append(urlT[0].decode())
			hashes.append(urlT[1].decode())
			i += 1
		if i == 0:
			time.sleep(0.1)
	return urls, hashes

def get_content(url):
	while True:
		try:
			req = requests.get(url)
			cont_type = req.headers.get('content-type')
			lang = "en"
			try:
				lang = req.headers.get('content-language')
			except:
				lang = "en"
			if "html" not in cont_type or lang != "en":
				return None
			elif req.content is not None:
				return str(req.content)
			else:
				t += 1
		except:
			t += 1
		if t == 4:
			try:
				requests.get("https://google.com")
				print("Page do not exist")
				return None
			except:
				print("No internet connection")
				time.sleep(0.5)
			break