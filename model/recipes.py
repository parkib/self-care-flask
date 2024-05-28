""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Recipe(db.Model):
    __tablename__ = 'recipes'  # table name is plural, class name is singular
    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _recipename = db.Column(db.String(255), unique=False, nullable=False)
    _healthyingredients = db.Column(db.String(255), unique=True, nullable=False)
    _recipesteps = db.Column(db.String(255), unique=False, nullable=False)
    _difficulty = db.Column(db.String(255), unique=False, nullable=False)
    _tags = db.Column(db.String(255), unique=False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, recipename, healthyingredients, recipesteps, difficulty, tags):
        self._recipename = recipename    # variables with self prefix become part of the object,
        self._healthyingredients = healthyingredients
        self._recipesteps = recipesteps
        self._difficulty = difficulty
        self._tags = tags
   
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


    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self, tags):
        self._tags = tags
        
        
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
            "recipename": self.recipename,
            "healthyingredients": self.healthyingredients,
            "recipesteps": self.recipesteps,
            "difficulty": self.difficulty,
            "tags": self.tags,
            
        }
    

"""Database Creation and Testing """
# Builds working data for testing
def initRecipes():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        recipes = [
            Recipe(recipename="Mango Smoothie", healthyingredients="mango, yogurt, honey", recipesteps="1. Peel and chop the mango. <br> 2. Blend the mango, yogurt, and honey until smooth.", difficulty="Easy", tags = "dairy-free,lunch" ),
            Recipe(recipename="Healthy Banana Muffins", healthyingredients="bananas, whole wheat flour, honey", recipesteps="1. Preheat oven to 350°F (175°C).  <br> 2. Mash bananas in a bowl.  <br> 3. Mix in whole wheat flour and honey until well combined.  <br> 4. Pour batter into muffin cups.  <br> 5. Bake for 20-25 minutes or until a toothpick inserted comes out clean.", difficulty="Intermediate", tags = "breakfast,cost-effective"),
            Recipe(recipename="Mushroom Kale Soup", healthyingredients="mushrooms, kale, vegetable broth", recipesteps="1. Slice mushrooms and chop kale.  <br> 2. In a large pot, sauté mushrooms until golden brown.  <br> 3. Add kale and vegetable broth to the pot.  <br> 4. Simmer for 20 minutes.  <br> 5. Season with salt and pepper to taste.", difficulty="Intermediate", tags = "dairy")
        ]
        """Builds sample user/note(s) data"""
        for recipe in recipes:
            try:
                recipe.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {recipe.recipename}")
            
