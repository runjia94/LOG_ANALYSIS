import psycopg2
from datetime import datetime

DBNAME = 'news'

def queryOperate(query):

	try:
		db = psycopg2.connect(database = DBNAME)
	except psycopg2.OperationalError as e:
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
		q1 = '1. what are the most popular three articles of all time?\n'
		f.write(q1)
		for item in topArticles:
			f.write(item[0] + ' --'+str(item[1]) + ' views \n')
		f.write('\n2. What are the most popular article authors of all time \n')
		for name in authorsRank:
			f.write(name[0]+' --' +str(name[1])+' views \n')
		f.write('\n3. On which days did more than 1% of requests lead to errors?\n')
		for error in errorcount:
			changetime = datetime.strptime(str(error[0]), '%Y-%m-%d').strftime('%B %d, %Y')
			f.write(changetime +' --'+ str(error[1])+'% errors')



