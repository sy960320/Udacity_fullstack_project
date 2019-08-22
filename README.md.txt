Reproting_Tool
A python program using the psycopg2 module to connect to the database 


Prerequisites:
    Python 3: https://www.python.org/downloads/
    Vagrant: https://www.vagrantup.com/downloads.html
    Virtual Box 3: https://www.virtualbox.org/
    Virtual Studio Code: https://visualstudio.microsoft.com/zh-hans/?rr=https%3A%2F%2Fwww.google.com%2F 


Supported by Python versions
    Python version 3.7.3
    https://www.python.org/downloads/ download newest version
    use "python --version" to check your python version on terminal

    
Useful Tool:
    Visual Studio - interpreted development environment, in this project we use it to programming SQL command    


Installation:
  Step1: install your vagrant on Git Bash
    open your terminal Git Bash
    set the path of vagrant on terminal use "PATH=$PATH..."
    change the current directory to the Virtual Machine directory which contain the "vagrant" folder
    input command to start the vagrant: 
        "mkdir vagrant_folder" 
        "cd vagrant_folder"
        "vagrant init ubuntu/trusty64"
        "vagrant up"
    The procedure above will help you install Virtual Machine environment on your terminal, once if you want to log into your vagrant just input command below 
        "vagrant ssh"

  Step2:
    Download newest Python version: https://www.python.org/downloads/
    Open your code editor, we use Visual Studio as the example.  
    Click "extension" and download "Python" on "Visual Studio".
    Click "Explorer" and click "open" option to chose a folder to storage
    Then you can create a new file in this folder with "file_name.py" 
    Now you coding Python program in this file. 


Execute the Program:
    When you dry to execute the Python program, we access vagrant to create a DB-API function to make conncetion between SQL and database.
    To access Vagrant we input command "vagrant ssh". 
    After you log into vagrant, change directry:
        "cd /vagrant"
    Finally, input command: 
        "python project.py" 
    

Coding Style:
    The first line must be "shebang"
    Because we are using psycopg2 module to connect the database, so we must "import psycopg2" before we programming
    

 View explaination: 
1. The first three method is for solve first question " What are the most popular three articles of all time?"
log_view() method contain a view that shows the traffic of user access on each articles 
  create view log_view as
  select path, count(*) access_number
  from log
  group by path
  order by path;

articles_view() method contain a view that make the article path corresponding to the article title, and find the most three popular articles of all time 
The CONCAT('/article/', articles.slug) will concatenate '/article/' sign with the article title of article.slug.
  create view articles_view as
  select articles.title, log_view.access_number
  from articles, log_view  
  where log_view.path = CONCAT('/article/', articles.slug)
  order by access_number desc
  limit 3;

2. In the middle three method solve the second question  "Who are the most popular article authors of all time?"
articles_view2() method contain a view that shows the webpage access view number of each articles, shows the author id which corresponding with the articles.  
  create view articles_view2 as
  select articles.author, articles.title, log_view.access_number
  from articles,log_view
  where log_view.path = CONCAT('/article/',articles.slug)
  order by access_number desc;

author_view() method contain a view that shows the most popular articles author, author.id is corresponding to article_view2.author 
  create view authors_view as
  select authors.name, sum(articles_view2.access_number) as view
  from authors, articles_view2
  where authors.id = articles_view2.author
  group by authors.name
  order by view desc;

3. The last four method solve the third question "Find the error rate of '404 NOT FOUND'"
error1() method contain a view, the 'error1' view shows the total number of '404 NOT FOUND' status every day.
date(time) make the time accuracy on date instead of second.
  create view error1 as
  select date(time), count(*) as error_number from log
  where status = '404 NOT FOUND'
  group by date(time)
  order by date(time);

error2() method contain a view, the 'error2' view count the total number of '200 OK' status in every day.
  create view error2 as
  select date(time), count(*) as total from log
  where status = '200 OK'
  group by date(time)
  order by date(time);

error_rate() method contain a view, the 'error_rate' view shows which days did more than 1% of requests lead to error. Calculate the error rate which use the error number from error1 view over divide the good status number from error2.
The view will show all days which more than 1% of requests lead to error. 
  create view e_rate as 
  select error1.date, (100.0*error1.error_number/error2.total) as rate 
  from error1, error2 
  where error1.date = error2.date 
  order by error1.date

Get_Post() method will output the answer to a text file named "output.txt"


Author: 
    Yang Song -- initial work


License:
    This project is licensed under the MIT License -- see the LICENSE file for detail
