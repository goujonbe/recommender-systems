import flask
from flask import Flask, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import TextField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://celia:postgres@localhost/web'

db = SQLAlchemy(app)
#curseur.execute("SELECT COUNT(customer_id) from customer WHERE customer_id=1 AND password='network';")
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    

    def __init__(self, customer_id, password):
        self.customer_id = customer_id
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.customer_id


#Table Movie
class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    title = db.Column(db.String(255))
    plot = db.Column(db.String(255))
    poster = db.Column(db.String(255))
    
    def __init__(self, movie_id, year,title,plot,poster):
        self.movie_id = movie_id
        self.year = year
        self.title = title
        self.plot = plot
        self.poster = poster
       
        
    def __repr__(self):
        return '<Movie %r>' % self.movie_id, '<Title : %r>' % self.title, '<poster %r>' % self.poster


#Table Actor
class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
     
    def __init__(self, actor_id, name):
        self.actor_id = actor_id
        self.name = name
                  
    def __repr__(self):
        return '<Actor %r>' % self.actor_id

#Table Director
class Director(db.Model):
    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
     
    def __init__(self, director_id, name):
        self.director_id = director_id
        self.name = name
     
    def __repr__(self):
        return '<Director %r>' % self.director_id

#Table Genre
class Genre(db.Model):
    director_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(255))
     
    def __init__(self, director_id, name):
        self.director_id = director_id
        self.genre = genre
     
    def __repr__(self):
        return '<Director %r>' % self.director_id
