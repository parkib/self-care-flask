""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    _recipename = db.Column(db.String(255), unique=False, nullable=False)
    _healthyingredients = db.Column(db.String(255), unique=False, nullable=False)
    _difficulty = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, recipename, healthyingredients, difficulty):
        self._recipename = recipename
        self._healthyingredients = healthyingredients
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
    def difficulty(self):
        return self._difficulty
    
    @difficulty.setter
    def difficulty(self, difficulty):
        self._difficulty = difficulty
    
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "recipename": self.recipename,
            "healthyingredients": self.healthyingredients,
            "difficulty": self.difficulty,
        }

def initRecipes():
    with app.app_context():
        db.create_all()
        R1 = Recipe(recipename="Mac and Cheese", healthyingredients="anchoviesfruits", difficulty="Hard"),
        R2 = Recipe(recipename="Pasta", healthyingredients="capsicumpepper", difficulty="Hard"),
        R3 = Recipe(recipename="Riloiu", healthyingredients="veggiesfruits", difficulty="Hard"),
        R4 = Recipe(recipename="Rilu", healthyingredients="veggrieserfruits", difficulty="easy"),
        R5 = Recipe(recipename="er", healthyingredients="verefggiesfrurfeits", difficulty="easy")
        recipes = [R1, R2, R3, R4, R5]
        for recipe in recipes:
            try:
                recipe.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Record exists")

