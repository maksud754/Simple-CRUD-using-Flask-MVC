import sqlite3 as sql

from model import *

from flask import Flask,render_template,request,redirect,jsonify


app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')
 
@app.route('/login', methods=['POST'])
def slogin():
    if checklogin(request.form['matricno'],request.form['password']):
        session['logged_in'] = True
        return render_template('home.html')
    else:
        flash('Wrong Password!!')
        return render_template('login.html',message='Opps invalid matricno or password!!')
        


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

@app.route('/students')
def student():
    rows=students()
    return render_template('view_students.html',rows=rows)

@app.route('/books')
def book():
    rows=books()
    return render_template('view_books.html',rows=rows)

@app.route('/borrow')
def bborrow():
    rows=borrow()
    return render_template('borrow_list.html',rows=rows)

@app.route('/new')
def new():
    row=['']*5
    status='0'
    return render_template('add_new_students.html',row=row,status=status)

@app.route('/update',methods=['GET','POST'])
def  insert_update():
    matricno = request.form['matricno']
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    password=request.form['password']
    
    if request.method=='POST' and request.form['status']=='0':                            
        row=['']*5
        row[0] = matricno
        row[1] = name
        row[2] = address
        row[3] = phone
        row[4] = password
    
        
        if matricno == '' or name == '' or password == '':
            msg = '';
            if matricno == '':
                msg += 'Matric No' if len(msg)==0 else ',Matric No'
            if name == '':
                msg += 'Name' if len(msg)==0 else ',Name'
            if password == '':
                msg += 'Password' if len(msg)==0 else ',Password'
            msg = msg + ' cannot be empty!!!';
            return render_template('add_new_students.html',message=msg,status='0',row=row)
        else:
            if check_matricno(matricno):
                row[0] = ''
                flash('Matric No already Exists!!')                
                return render_template('add_new_students.html',message='Matric No '+matricno+' already exists!!!',status='0',row=row)

            else:        
                insert_student(matricno,name,address,phone,password)        
                return redirect('/students')
      
    if request.method=='POST' and request.form['status']=='0':                            
          
        insert_student(matricno,name,address,phone,password)
        return redirect('/students')
        
        
          
    if request.method=="POST" and request.form['status']=='1':
        update_student(name,address,phone,password,matricno)
        return redirect('/students')
    
@app.route('/edit/<matricno>')
def edits(matricno): 
    row=find_student(matricno)
    status='1'
    return render_template('add_new_students.html',row=row,status=status)

@app.route('/delete/<matricno>')
def  delete(matricno):  
     delete_student(matricno)
     return redirect('/students')

@app.route('/find_student',methods=['GET','POST'])
def find():
    if request.method=="POST":
        matricno=request.form['matricno']
        row=find_student(matricno)
        return render_template('resultstudent.html',row=row)
    else:   
        return render_template('findstudents.html')

@app.route('/new_book')
def newb():
    row=['']*6
    status='0'
    return render_template('add_new_books.html',row=row,status=status)

@app.route('/update_book',methods=['GET','POST'])
def  insert_bupdate():
    isbn = request.form['isbn']
    title = request.form['title']
    year = request.form['year']
    author = request.form['author']
    publisher=request.form['publisher']
    publish_date=request.form['publish_date']
    
    if request.method=='POST' and request.form['status']=='0':                            
        row=['']*6
        row[0] = isbn
        row[1] = title
        row[2] = year
        row[3] = author
        row[4] = publisher
        row[5] = publish_date
    
        
        if isbn == '' or title == '' or author == '':
            msg = '';
            if isbn == '':
                msg += 'ISBN' if len(msg)==0 else ',ISBN'
            if title == '':
                msg += 'Title' if len(msg)==0 else ',Title'
            if author == '':
                msg += 'Author' if len(msg)==0 else ',Author'
            msg = msg + ' cannot be empty!!!';
            return render_template('add_new_books.html',message=msg,status='0',row=row)
        else:
            if check_isbn(isbn):
                row[0] = ''
                flash('This Book already Exists!!')                
                return render_template('add_new_books.html',message='ISBN '+isbn+' already exists!!!',status='0',row=row)

            else:        
                insert_book(isbn,title,year,author,publisher,publish_date)        
                return redirect('/books')
      
    if request.method=='POST' and request.form['status']=='0':                            
          
        insert_book(isbn,title,year,author,publisher,publish_date)
        return redirect('/books')
        
        
          
    if request.method=="POST" and request.form['status']=='1':
        update_books(title,year,author,publisher,publish_date,isbn)
        return redirect('/books')
    
@app.route('/edit_book/<isbn>')
def editb(isbn): 
    row=find_book(isbn)
    status='1'
    return render_template('add_new_books.html',row=row,status=status)

@app.route('/delete_book/<isbn>')
def  deleteb(isbn):  
     delete_book(isbn)
     return redirect('/books')


@app.route('/find_book',methods=['GET','POST'])
def bfind():
    if request.method=="POST":
        isbn=request.form['isbn']
        row=find_book(isbn)
        return render_template('result_book.html',row=row)
    else:   
        return render_template('find_books.html')
    



if __name__ == "__main__":
     app.secret_key = "!makko09098909"
     app.run(debug=True)

