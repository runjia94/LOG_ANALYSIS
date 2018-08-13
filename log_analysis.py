import psycopg2

DBNAME = 'news'

def queryOperate(query):

	try:
		db = psycopg2.connect(database = DBNAME)
	except psycopg2.OperationalError as e:
		#Exception raised for errors that are related to the database’s operation and not necessarily under the control of the programmer
		print "there is an error when connect to database"+ DBNAME
		print e

	c = db.cursor()
	c.execute(query)
	result = c.fetchall()
	db.close()
	return result


def top_articles():
	query = """ SELECT articles.title, COUNT(*) AS views
				FROM articles JOIN log
				ON log.path = '/article/' || articles.slug
				WHERE log.status LIKE '200%'
				GROUP BY articles.title
				ORDER BY views DESC
				LIMIT 3;"""

	topArticles = queryOperate(query)
	return topArticles


def topAuthors():
	query = """ SELECT authors.name, COUNT(*) AS views 
				FROM authors 
				JOIN articles ON articles.author = authors.id 
				JOIN log ON log.path = '/article/' || articles.slug 
				WHERE log.status LIKE '200%' 
				GROUP BY authors.name 
				ORDER BY views DESC;"""
	authorsRank = queryOperate(query)
	return authorsRank


def errorLimit():
	query = """ SELECT day, percent FROM(
				SELECT day, ROUND(
				(SUM(error)/(SELECT COUNT(*) FROM log 
				WHERE time::date = day)*100),2) AS percent FROM (
				SELECT time::date AS day, 
				COUNT(*) AS error 
				FROM log 
				WHERE status LIKE '%404%' 
				GROUP BY day)
				AS percentlist
				GROUP BY day
				ORDER BY percent DESC)
				AS result
				WHERE percent >= 1;"""
	errorcount = queryOperate(query)
	return errorcount


if __name__ == '__main__':
	topArticles = top_articles()
	authorsRank = topAuthors()
	errorcount = errorLimit()

	with open('output.txt','w') as f:
		q1 = 'what are the most popular three articles of all time?'
		f.write(q1)
		f.write(topArticles)



