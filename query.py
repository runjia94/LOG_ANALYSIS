
'''FOCUS: THIS IS THE SCRIPT FOR SOLVING PROBLEMS, NOT SOLUTION!



what the most popular articles of all time 
              title               | views  
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098

 
select articles.title, count(*) as views
from articles join log
on log.path = '/article/' || articles.slug
where log.status like '200%'
group by articles.title
order by views desc
limit 3;
'''



'''
          name          | views  
------------------------+--------
 Ursula La Multa        | 507594
 Rudolf von Treppenwitz | 423457
 Anonymous Contributor  | 170098
 Markoff Chaney         |  84557


 elect authors.name, count(*) as views from authors join articles on articles.author = authors.id joisn log on log.path = '/article/' || articles.slug where log.status like '200%' group by authors.name order by views desc;
 '''

 """
 This is the question3  step by step

 select date_trunc('day',log.time) as day,count(*) as numbers from log group by day order by numbers desc;
 select date_trunc('day',log.time) as day,count(*) as numbers from log where log.status like '200%' group by day order by numbers desc;

 select 1 : (select time::date as day, count(*) as error from log where status like '404%' group by day) as percentlist;

 select 2: select day,round((sum(error)/(select count(*) from log where time::date = day)*100),2) as percent from select1 group by day;
 
 select 3: select day,percent from (select2 order by percent desc) as result where percent >=1

SELECT day, percent FROM(
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
WHERE percent >= 1;











