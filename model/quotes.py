""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash



class Quote(db.Model):
    __tablename__ = 'quotes'  # table name is plural, class name is singular
    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _quotename = db.Column(db.String(255), unique=False, nullable=False)
    _quoteauthor = db.Column(db.String(255), unique=True, nullable=False)
    _opinion = db.Column(db.String(255), unique=False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, quotename, quoteauthor, opinion):
        self._quotename = quotename    # variables with self prefix become part of the object,
        self._quoteauthor = quoteauthor
        self._opinion = opinion
   
    @property
    def quotename(self):
        return self._quotename
    @quotename.setter
    def quotename(self, quotename):
        self._quotename = quotename
         
    @property
    def quoteauthor(self):
        return self.quoteauthor
    @quoteauthor.setter
    def quoteauthor(self, quoteauthor):
        self._quoteauthor = quoteauthor

    @property
    def opinion(self):
        return self._opinion
    @opinion.setter
    def opinion(self, opinion):
        self._opinion = opinion
        
    def __str__(self):
        return json.dumps(self.read())


    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
    

    def read(self):
        return {
            "id": self.id,
            "quotename": self.quotename,
            "quoteauthor": self.quoteauthor,
            "opinion": self.opinion,
            
        }
    

"""Database Creation and Testing """
# Builds working data for testing
def initQuotes():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        quotes = [
            Quote(quotename="Carpe Diem", quoteauthor="Horous", opinion="Quote's very great!"),
        ]
        """Builds sample user/note(s) data"""
        for quote in quotes:
            try:
                quote.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {quote}")
            