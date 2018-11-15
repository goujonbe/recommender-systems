import flask
from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
import sqlite3 
from flask import render_template
from sqlalchemy import and_
from creation_bd import Customer
from creation_bd import Movie
from creation_bd import db
from creation_bd import app
from sqlalchemy import func 


@app.route('/', methods=['GET', 'POST'])
def start():
    
    
    if request.method == 'POST':
        
        customer_is_in_db = Customer.query.filter(and_(
            Customer.customer_id==int(request.form['customer_id']),
            Customer.password==request.form['password'])
            ).count()

        if (not(customer_is_in_db)):
            error = 'Invalid Credentials. Please try again.'
            print("ko")
            return render_template('start.html', error=error)
         
        else:
            return redirect(url_for('home'))
            print("ok")
    return render_template('start.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # customer_already_exist = Customer.query.filter(
        #     Customer.customer_id==int(request.form['customer_id']))


        liste = db.session.query(Customer.customer_id).all()
        ids = [id[0] for id in liste]
        print(ids)
        if (int(request.form['customer_id']) in ids):
            error = 'Invalid Credentials. Please try again.'
            print("ko")
            return render_template('signup.html', error=error)
        else:
            new_customer = Customer(int(request.form['customer_id']),request.form['password'])
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('taste'))
            
    
    id_max = db.session.query(func.max(Customer.customer_id)).first()
    print(id_max)
    print(type(id_max))
    new_id = int(id_max[0]) + 1        
    return render_template('signup.html', new_id=new_id)

@app.route('/account/')
def account():
    return render_template('about.html')

@app.route('/movie/')
def movie():
    case_movie = db.session.query.filter(Movie.title=="Pulp Fiction").all()
    print(case_movie)
    return render_template('movie.html')

@app.route('/taste/')
def taste():
    
    liste_title = db.session.query(Movie.title).all()
    title = [titre[0] for titre in liste_title]
    
    liste_poster = db.session.query(Movie.poster).all()
    poster = [affiche[0] for affiche in liste_poster]

    liste_plot = db.session.query(Movie.plot).all()
    plot = [resume[0] for resume in liste_plot]
    print(title)
    print(poster)
    print(plot)

    return render_template('taste.html',liste_title=liste_title,title=title,poster=poster, plot=plot)


@app.route('/home/', methods=["GET"])
#return render_template('hello.html', name=name)
def home():
    return render_template('index.html')




