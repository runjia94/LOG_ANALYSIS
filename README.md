LOG ANALYSIS
=============

This is a project which is designed for a backend developer. 
The database comes from a newspaper website. We need to use **SQL** to query data from this database to get the result.

There are three questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors? 

this project comes from Udacity - [Full Stack Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

Technology
----------
* SQL(Postgresql)
* Python
* vagrant
* VirtualBox

Pre-request
-----------
* Download [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Download [vagrant](https://www.vagrantup.com/downloads.html)
* Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.
Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.
From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.
When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!

* newspaper database is [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
To load the data, cd into the vagrant directory and use the command psql -d news -f newsdata.sql.
Once you have the data loaded into your database, connect to your database using psql -d news and explore the tables using the \dt and \d table commands and select statements.

Query
------

* What the most popular articles of all time 
```sql
select articles.title, count(*) as views
from articles join log
on log.path = '/article/' || articles.slug
where log.status like '200%'
group by articles.title
order by views desc
limit 3;
```
* Who are the most popular article authors of all time? 
```sql
SELECT authors.name, COUNT(*) AS views 
FROM authors 
JOIN articles ON articles.author = authors.id 
JOIN log ON log.path = '/article/' || articles.slug 
WHERE log.status LIKE '200%' 
GROUP BY authors.name 
ORDER BY views DESC
```

* On which days did more than 1% of requests lead to errors?
```sql
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
WHERE percent >= 1;"""
```

* For detail in question3, you can see the file named query.py

RUN METHOD
___________

After you run psql -d news -f newsdata.sql.
Then run psql -d news. You will find the command line turns to news=>
it means you have connected to this database.
Then you can try query sentence in the query.py

You should use control D to quit this database.
Then run 'python log_analysis.py', of course , without quotation mark.
Then you will get a output.txt file. The result is in this file.