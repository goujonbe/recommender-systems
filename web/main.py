import flask
from flask import Flask, url_for
app = Flask(__name__)


from flask import request
import sqlite3 
from flask import render_template

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/account/')
def account():
    return render_template('about.html')

@app.route('/movie/')
def movie():
    return render_template('movie.html')

@app.route('/taste/')
def taste():
    return render_template('taste.html')


@app.route('/home/', methods=["POST","GET"])
#return render_template('hello.html', name=name)
def home():
    file = open("/home/celia/pfe/formated/combined_data_1.csv","r") 
    db = sqlite3.connect('/home/celia/pfe/start/web/netflix.db')

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS client;')
    db.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client(movie_id INTEGER, customer_id INTEGER,rating INTEGER,date date);
    ''')
    db.commit()


    cursor = db.cursor()

    
    # Insert user 1
    cursor.execute('''INSERT INTO client(movie_id,customer_id, rating, date)
                    VALUES(?,?,?,?)''', (1,2,3, "2005-09-06"))
    print('First user inserted')
    
    # Insert user 2
    cursor.execute('''INSERT INTO client(movie_id,customer_id, rating, date)
                    VALUES(?,?,?,?)''', (2,5,7, "2005-09-06"))
    print('Second user inserted')
    
    db.commit()

    db.close()


    return render_template('index.html')




