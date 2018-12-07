import flask
from flask import Flask, session, redirect, url_for, escape, request
from flask_sqlalchemy import SQLAlchemy
from flask import request
import sqlite3 
from flask import render_template
from sqlalchemy import and_
from creation_bd import Customer,Movie,Rate,db,app
from sqlalchemy import func 
from datetime import datetime
from datetime import date
import requests

app.secret_key = b'pfe_netflix'


@app.route('/', methods=['GET', 'POST'])
def start():
    
    
    if request.method == 'POST':
        
        customer_is_in_db = Customer.query.filter(and_(
            Customer.customer_id==int(request.form['customer_id']),
            Customer.password==request.form['password'])
            ).count()
        
        session['customer_id'] = int(request.form['customer_id'])

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

@app.route('/movie/<int:movie_id>', methods=['GET','POST'])
def movie(movie_id):
    #case_movie = db.session.query.filter(Movie.title=="Pulp Fiction").all()
    #print(case_movie)

         
    if request.method == 'POST':
        note = int(request.form['rating'])
        print('note =', note)
        print('customer_id =', session['customer_id'])
        print('movie id = ', movie_id)
        date = datetime.now()
        print(date)

        new_rate = Rate(session['customer_id'],movie_id,int(note),date)
        db.session.add(new_rate)
        db.session.commit()


    else:
        movie_data = db.session.query(Movie.movie_id, Movie.poster, Movie.year, Movie.title, Movie.plot)\
        .filter(Movie.movie_id == movie_id)\
        .first()

        print(movie_data)


    
    return render_template('movie.html', movie_data=movie_data)

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


@app.route('/home/', methods=['GET'])
#return render_template('hello.html', name=name)
def home():
    customer_id = session['customer_id']
    requete_api = requests.get('http://127.0.0.1:5001/{}'.format(customer_id))
    movies = requete_api.json()['{}'.format(customer_id)]
    print(movies)
    movies_in_db = db.session.query(Movie.movie_id, Movie.poster, Movie.title) \
    .filter(Movie.movie_id.in_(movies))\
    .all()  



    return render_template('index.html', movies=movies_in_db)




