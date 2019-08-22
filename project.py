#!/usr/bin/env python3
import psycopg2

DBNAME = 'news'


# 1. What are the most popular three articles of all time?
def log_view(content):
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute("create view log_view as select path, count(*) as access_number from log group by path order by path;")
    conn.commit()
    conn.close()


def articles_view(content):
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute("create view articles_view as select articles.title, log_view.access_number from articles, log_view where log_view.path = CONCAT('/article/', articles.slug) order by access_number desc limit 3")
    conn.commit()
    conn.close()


# 2. Who are the most popular article authors of all time?
def articles_view2(content):
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute("create view articles_view2 as select articles.author, articles.title, log_view.access_number from articles,log_view where log_view.path = CONCAT('/article/',articles.slug) order by access_number desc")
    conn.commit()
    conn.close()


def authors_view(content):
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute("create view authors_view as select authors.name, sum(articles_view2.access_number) as view from authors, articles_view2 where authors.id = articles_view2.author group by authors.name order by view desc")
    conn.commit()
    conn.close()


# 3. Find the error rate of '404 NOT FOUND'
def error1(content):
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute("create view error1 as select date(time), count(*) as error_number from log where status = '404 NOT FOUND' group by date(time) order by date(time)")
    conn.commit()
    conn.close()


def error2(content): 
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute("create view error2 as select date(time), count(*) as total from log group by date(time) order by date(time)")
    conn.commit()
    conn.close()


def error_rate(content): 
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute("create view e_rate as select error1.date, (100.0*error1.error_number/error2.total) as rate from error1, error2 where error1.date = error2.date order by error1.date")
    conn.commit()
    conn.close()


def Get_post():
    File = open("output.txt", "w")
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    File.write("What are the most popular three articles of all time?:\n")
    cursor.execute("select * from articles_view")
    result = cursor.fetchall()
    output = ""
    for data in result:
        output += str(data)
        output += "\n"
    File.write(output)
    File.write("\n")
    File.write("Who are the most popular article authors of all time?\n")
    cursor.execute("select * from authors_view\n")
    result = cursor.fetchall()
    output = ""
    for data2 in result:
        output += str(data2)
        output += "\n"
    File.write(output)
    File.write("\n")
    File.write("Find the error rate of '404 NOT FOUND':\n")
    cursor.execute("select date, rate from e_rate where rate = (select max(rate) from e_rate)")
    result = cursor.fetchall()
    output = ""
    for data3 in result:
        output += str(data3)
        output += "\n"
    File.write(output)
    File.close()
    File = open("output.txt", "r")
    print(File.read())
    conn.close()


Get_post()
