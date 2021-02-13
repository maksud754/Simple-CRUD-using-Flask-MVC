import sqlite3 as sql

from functools import wraps
from flask import session,flash,redirect,url_for

connect_db ='byb.db'

def checklogin(matricno,password):
  with sql.connect(connect_db) as db: 
    qry = 'select matricno,pass from students where matricno=? and pass=?'
    result=db.execute(qry,(matricno,password)).fetchone()
    return(result)

def students():
 with sql.connect(connect_db) as db:
    qry = 'select * from students' 
    result=db.execute(qry)
    return(result)

def books():
 with sql.connect(connect_db) as db:
    qry = 'select * from book' 
    result=db.execute(qry)
    return(result)

def borrow():
 with sql.connect(connect_db) as db:
    qry = 'select * from borrow'
    result=db.execute(qry)
    return(result)


def insert_student(matricno,name,address,phone,password):
  with sql.connect(connect_db) as db:
    qry='insert into students (matricno,name,address,phone,pass) values (?,?,?,?,?)' 
    db.execute(qry,(matricno,name,address,phone,password))

def update_student(matricno,name,address,phone,password):
  with sql.connect(connect_db) as db:
    qry='update students set name=?,address=?,phone=?,pass=? where matricno=?' 
    db.execute(qry, (matricno,name,address,phone,password))
    
def find_student(matricno):
  with sql.connect(connect_db) as db:
    qry = 'select * from students where matricno=?'
    result=db.execute(qry,(matricno,)).fetchone()
    return(result)

def check_matricno(matricno):
  with sql.connect(connect_db) as db: 
    qry = 'select matricno,pass from students where matricno=?'
    result=db.execute(qry,(matricno,)).fetchone()
    return(result)

def delete_student(matricno):
  with sql.connect(connect_db) as db:
    qry='delete from students where matricno=?' 
    db.execute(qry,(matricno,))

def insert_book(isbn,title,year,author,publisher,publish_date):
  with sql.connect(connect_db) as db:
    qry='insert into book (isbn,title,year,author_name,publisher_name,publish_date) values (?,?,?,?,?,?)' 
    db.execute(qry,(isbn,title,year,author,publisher,publish_date))

def update_books(isbn,title,year,author,publisher,publish_date):
  with sql.connect(connect_db) as db:
    qry='update book set title=?,year=?,author_name=?, publisher_name=?,  publish_date=? where isbn=?' 
    db.execute(qry, (isbn, title,year,author,publisher,publish_date))

def check_isbn(isbn):
  with sql.connect(connect_db) as db: 
    qry = 'select isbn from book where isbn=?'
    result=db.execute(qry,(isbn,)).fetchone()
    return(result)

def delete_book(isbn):
  with sql.connect(connect_db) as db:
    qry='delete from book where isbn=?' 
    db.execute(qry,(isbn,))
    
def find_book(isbn):
  with sql.connect(connect_db) as db:
    qry = 'select * from book where isbn=?'
    result=db.execute(qry,(isbn,)).fetchone()
    return(result)

def result():
    rows=students()
    rows=books()
    rows=borrow()
    for row in rows:
        print (row)






def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
        return f(*args, **kwargs)
    else:
        flash("You need to login first")
        return redirect(url_for('home'))
  return wrap
