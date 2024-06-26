""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

class Therapy(db.Model):
    __tablename__ = 'therapies'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _location = db.Column(db.String(255), unique=False, nullable=False)
    _special = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, name, location, special):
        self._name = name
        self._location = location
        self._special = special

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, location):
        self._location = location
    
    @property
    def special(self):
        return self._special
    
    @special.setter
    def special(self, special):
        self._special = special
    
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
            "location": self.location,
            "special": self.special,
        }

def initTherapies():
    with app.app_context():
        db.create_all()
        therapies = [
            Therapy(name="Tranquil Haven Counseling Center", location="Suburban Retreat", special="General Counseling"),
            Therapy(name="Healing Waters Retreat", location="Riverside Sanctuary", special="Trauma Recovery"),
            Therapy(name="Family Harmony Center", location="Urban Oasis", special="Family Counseling"),
            Therapy(name="Sunrise Serenity Therapy Spa", location="Coastal Resort", special="Wellness Retreat"),
            Therapy(name="Inner Peace Sanctuary", location="Mountain Retreat", special="Mindfulness Therapy"),
            Therapy(name="Empowerment Pathways Center", location="Downtown Hub", special="Personal Growth Workshops"),
            Therapy(name="Whispering Winds Wellness Retreat", location="Countryside Haven", special="Stress Management"),
            Therapy(name="Safe Harbor Trauma Center", location="Seaside Refuge", special="PTSD Treatment"),
            Therapy(name="Hope Springs Counseling Oasis", location="Desert Sanctuary", special="Grief Counseling"),
            Therapy(name="Bright Horizons Counseling Collective", location="Community Center", special="Youth Counseling"),
            Therapy(name="Serenity Falls Therapy Retreat", location="Forest Hideaway", special="Addiction Recovery"),
            Therapy(name="Lighthouse Healing Institute", location="Lakeside Sanctuary", special="Depression Support"),
            Therapy(name="Tranquility Cove Wellness Center", location="Island Escape", special="Anxiety Relief"),
            Therapy(name="Phoenix Rising Counseling Center", location="Metropolitan Haven", special="Life Coaching"),
            Therapy(name="Golden Pathways Therapy Haven", location="Retreat Center", special="Spiritual Counseling")
        ]
        for therapy in therapies:
            try:
                therapy.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Record exists")

