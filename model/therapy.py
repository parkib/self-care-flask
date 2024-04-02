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
    _specialization = db.Column(db.String(255), unique=False, nullable=False)
    _therapists = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, name, location, specialization, therapists):
        self._name = name
        self._location = location
        self._specialization = specialization
        self._therapists = therapists

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
    def specialization(self):
        return self._specialization
    
    @specialization.setter
    def specialization(self, specialization):
        self._specialization = specialization
    
    @property
    def therapists(self):
        return self._therapists
    
    @therapists.setter
    def therapists(self, therapists):
        self._therapists = therapists
    
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
            "specialization": self.specialization,
            "therapists": self.therapists,
        }

def initTherapy():
    with app.app_context():
        db.create_all()
        activities = [
            Therapy(name='KMG Psychiatry', location="6496 Weathers Pl Suite 100 & 110, San Diego, CA 92121", specialization="True", thrapists="False"),
        ]
        for activity in activities:
            try:
                activity.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Record exists")

