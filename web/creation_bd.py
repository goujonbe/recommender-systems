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

