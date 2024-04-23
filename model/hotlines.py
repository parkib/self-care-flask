""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
class Hotline(db.Model):
    __tablename__ = 'hotlines'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _number = db.Column(db.String(255), unique=False, nullable=False)
    def __init__(self, name, number):
        self._name = name
        self._number = number
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
    @property
    def number(self):
        return self._number
    @number.setter
    def location(self, number):
        self._number = number
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
            "name": self.name,
            "number": self.number,
        }
def initHotlines():
    with app.app_context():
        db.create_all()
        R1 = Hotline(name="National Domestic Violence Hotline", number="1-800-799-SAFE"),
        R2 = Hotline(name="Elder Abuse Hotline", number="1-800-252-8966"),
        R3 = Hotline(name="Eating Disorders Awareness and Prevention", number="1-800-931-2237"),
        R4 = Hotline(name="Family Violence Prevention Center", number="1-800-313-1310"),
        R5 = Hotline(name="Compulsive Gambling Hotline", number="1-410-332-0402"),
        R6 = Hotline(name="Homeless", number="1-800-231-6946"),
        R7 = Hotline(name="American Family Housing", number="1-888-600-4357"),
        ## Hotline(name="GriefShare", number="1-800-395-5755"),
        ## Hotline(name="United STates Missing Children Hotline", number="1-800-235-3525"),
        hotlines = [R1, R2, R3, R4, R5, R6, R7]
        for hotline in hotlines:
            try:
                hotline.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Record exists")