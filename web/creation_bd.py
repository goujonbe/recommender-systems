import flask
from flask import Flask, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import TextField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import DateTime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://celia:postgres@10.78.104.21/web'

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
    imdbrating = db.Column(db.Float,default='0')
    imdbvotes = db.Column(db.Integer)
    
    def __init__(self, movie_id, year,title,plot,poster, imdbrating, imdbvotes):
        self.movie_id = movie_id
        self.year = year
        self.title = title
        self.plot = plot
        self.poster = poster
        self.imdbrating = imdbrating
        self.imdbvotes = imdbvotes
       
        
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
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(255))
         
    def __init__(self, genre_id,genre_name):
        self.genre_id = genre_id
        self.genre_name = genre_name
     
    def __repr__(self):
        return '<Director %r>' % self.genre_name


#Table rate
class Rate(db.Model):
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.customer_id'), primary_key=True )
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    rating = db.Column(db.Integer, default='0')
    date = db.Column(db.DateTime, index=True)

    db.relationship('Customer')
    db.relationship('Movie')
     
    def __init__(self, customer_id, movie_id,rating,date):
        self.customer_id = customer_id
        self.movie_id = movie_id
        self.rating = rating
        self.date = date

     
    def __repr__(self):
        return '<Director %r>' % self.rating


#Table like_director
class Like_director(db.Model):
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id'),primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)

    db.relationship('Director')
    db.relationship('Customer')
         
   
    def __init__(self, director_id, name):
        self.customer_id = customer_id
        self.director_id = director_id
             
    def __repr__(self):
        return '<Director %r>' % self.director_id

#Table like_genre
class Like_genre(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)
    
   
    db.relationship('Genre')
    db.relationship('Customer')

    def __init__(self, genre_id, customer_id):
        self.genre_id = genre_id
        self.customer_id = customer_id
             
    def __repr__(self):
        return '<Director %r>' % self.genre_id

#Table like_actor
class Like_actor(db.Model):
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)

    db.relationship('Actor')
    db.relationship('Customer')
   
    def __init__(self, actor_id, customer_id):
        self.actor_id = actor_id
        self.customer_id = customer_id
             
    def __repr__(self):
        return '<Director %r>' % self.actor_id


#Table direct
class Direct(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id'), primary_key=True)

    db.relationship('Movie')
    db.relationship('Director')
   
    def __init__(self, movie_id, director_id):
        self.movie_id = movie_id
        self.director_id = director_id
             
    def __repr__(self):
        return '<Director %r>' % self.movie_id

#Table play
class Play(db.Model):
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    
    db.relationship('Movie')
    db.relationship('Actor')

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id
             
    def __repr__(self):
        return '<Director %r>' % self.movie_id

#Table has
class Has(db.Model):
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    
    db.relationship('Movie')
    db.relationship('Genre')
   
    def __init__(self, movie_id, genre_id):
        self.movie_id = movie_id
        self.genre_id = genre_id
             
    def __repr__(self):
        return '<Director %r>' % self.movie_id










