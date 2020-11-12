import mysql.connector

db = mysql.connector.connect(host="localhost",
  user="root",
  passwd="",
  database='web')


cursor = db.cursor()
totalWords = "SELECT COUNT(*) FROM words"
totalUrls = "SELECT COUNT(*) FROM urls"
totalLinks = "SELECT COUNT(*) FROM links"
visitedUrls = "SELECT COUNT(*) FROM urls WHERE visited = 1"

cursor.execute(totalWords)
rslt = cursor.fetchall()
nWords0 = max(int(rslt[0][0]), 1)
cursor.execute(totalUrls)
rslt = cursor.fetchall()
nLinks0 = max(int(rslt[0][0]), 1)
cursor.execute(totalLinks)
rslt = cursor.fetchall()
nUrls0 = max(int(rslt[0][0]), 1)
cursor.execute(visitedUrls)
rslt = cursor.fetchall()
nVisited0 = max(int(rslt[0][0]), 1)

