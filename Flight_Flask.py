import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import sqlite3 as sql

conn = sqlite3.connect('flight.db')
print ("Opened database successfully");

#conn.execute('CREATE TABLE flights (flight_num TEXT, org_airport TEXT, dest_airport TEXT, status TEXT)')
print ("Table created successfully");
conn.close()

con = sql.connect("flight.db")
con.row_factory = sql.Row

app = Flask(__name__)
@app.route('/enternew_flight')

def new_student():
   return render_template('flight.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         flight_num = request.form['flight_num']
         oa = request.form['oa']
         da = request.form['da']
         status = request.form['status']
         
         with sql.connect("flight.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO flights (flight_num, org_airport, dest_airport, status) VALUES (?,?,?,?)",(flight_num,oa,da,status) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("flight_result.html",msg = msg)
         con.close()

@app.route('/list_status')
def list():
   con = sql.connect("flight.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from flights")
   
   rows = cur.fetchall(); 
   #for row in cur.execute('''
   #   select * from students
   #   '''):
   # print(row)
   return render_template("list_status.html",rows = rows)

#@app.route('/')
#def home():
#   return render_template('home.html')


if __name__ == "__main__":
    app.run()
