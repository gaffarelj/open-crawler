from tld import get_tld
import hashlib
import mysql.connector

db = mysql.connector.connect(host="localhost",
  user="root",
  passwd="",
  database='web')

def get_hash(url):
	return hashlib.sha256(url.encode()).hexdigest()

def get_domain(url):
	try:
		return get_tld(url, as_object=True).fld
	except:
		return None
	return None

def get_id(hash):
	cursor = db.cursor()
	cursor.execute("SELECT id FROM urls WHERE hash = '" + hash + "'")
	return cursor.fetchone()[0]

def save_urls(urls, url_id):
	cursor = db.cursor()
	url_param = []
	link_param = []
	for url in urls:
		if url is not None and url != "" and hash is not None:
			hashT = get_hash(url)
			domain = get_domain(url)
			if domain is not None:
				url_param.append((url, hashT, domain))
				link_param.append((url_id, hashT))
	saveUrls = "INSERT IGNORE INTO urls (url, hash, domain) VALUES (%s, %s, %s)"
	saveLinks = "INSERT IGNORE INTO links (from_id, to_id) VALUES (%s, (SELECT id FROM urls WHERE hash = %s))"
	deletePrevious = "DELETE FROM links WHERE from_id = " + str(url_id)
	urlDone = "UPDATE urls SET visited = 1, last_visit = NOW(), to_visit = 0 WHERE id = %s" % url_id
	cursor.execute(deletePrevious)
	cursor.execute(urlDone)
	cursor.executemany(saveUrls, url_param)
	cursor.executemany(saveLinks, link_param)

def save_words(words, weights, url_id):
	cursor = db.cursor()
	param = list(zip(words, words, weights))
	deletePrevious = "DELETE IGNORE FROM words WHERE url_id = " + str(url_id) + "; DELETE IGNORE FROM words WHERE weight = 0"
	cursor.execute(deletePrevious, multi=True)
	saveWords = "INSERT IGNORE INTO words (url_id, word_id, weight) VALUES (" + str(url_id) + ", (SELECT id FROM dictionary WHERE word = %s), (SELECT importance FROM dictionary WHERE word = %s)*%s)"
	cursor.executemany(saveWords, param)
	cursor.execute("DELETE FROM words WHERE word_id = 0")