""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash



class Qt1():
    _qt1name = db.Column(db.String(255), unique=False, nullable=False)
    def __init__(self, qt1name):
        self._qt1name = qt1name    # variables with self prefix become part of the object,
   
    @property
    def qt1name(self):
        return self._qt1name
    @qt1name.setter
    def qt1name(self, qt1name):
        self._qt1name = qt1name        
        
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            return self
        except IntegrityError:
            return None
    

    def read(self):
        return {
            "qt1name": "test",            
        }
    

"""Database Creation and Testing """
# Builds working data for testing
def initqt1s():
    print("Error in init qt1s")
