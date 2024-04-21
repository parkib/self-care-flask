""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''
# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Recipe(db.Model):
    __tablename__ = 'recipes'  # table name is plural, class name is singular
    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _recipename = db.Column(db.String(255), unique=False, nullable=False)
    _healthyingredients = db.Column(db.String(255), unique=True, nullable=False)
    _recipesteps = db.Column(db.String(255), unique=False, nullable=False)
    _difficulty = db.Column(db.String(255), unique=False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, recipename, healthyingredients, recipesteps, difficulty ):
        self._recipename = recipename    # variables with self prefix become part of the object,
        self._healthyingredients = healthyingredients
        self._recipesteps = recipesteps
        self._difficulty = difficulty
   
    @property
    def recipename(self):
        return self._recipename
    @recipename.setter
    def recipename(self, recipename):
        self._recipename = recipename
         
    @property
    def healthyingredients(self):
        return self._healthyingredients
    @healthyingredients.setter
    def healthyingredients(self, healthyingredients):
        self._healthyingredients = healthyingredients

    @property
    def recipesteps(self):
        return self._recipesteps
    @recipesteps.setter
    def recipesteps(self, recipesteps):
        self._recipesteps = recipesteps
    
    @property
    def difficulty(self):
        return self._difficulty
    @difficulty.setter
    def difficulty(self, difficulty):
        self._difficulty = difficulty
        
        

  
    #property is returned as string, to avoid unfriendly outcomes
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "recipename": self.recipename,
            "healthyingredients": self.healthyingredients,
            "recipesteps": self.recipesteps,
            "difficulty": self.difficulty,
            
        }
    # CRUD update: updates user name, password, phone
    # returns self

"""Database Creation and Testing """
# Builds working data for testing
def initRecipes():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        recipes = [
            Recipe(recipename="mi", healthyingredients="none", recipesteps="hsfeat", difficulty="il"),
            Recipe(recipename="hjbmi", healthyingredients="nonhke", recipesteps="hebhsfd,at", difficulty="ihl,l"),
            Recipe(recipename="mhki", healthyingredients="nonehk", recipesteps="hehgjat", difficulty="ijkhl")
        ]
        """Builds sample user/note(s) data"""
        for recipe in recipes:
            try:
                recipe.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {recipe.recipename}")
            