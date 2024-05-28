from random import randrange
from datetime import date
import os, base64
import json


from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    _quotename = db.Column(db.String(255), unique=False, nullable=False)
    _quoteauthor = db.Column(db.String(255), unique=False, nullable=False)
    _opinion = db.Column(db.String(255), unique=False, nullable=False)
    _rating = db.Column(db.Integer, nullable=False)


    def __init__(self, quotename, quoteauthor, opinion, rating):
        self._quotename = quotename
        self._quoteauthor = quoteauthor
        self._opinion = opinion
        self._rating = rating


    @property
    def quotename(self):
        return self._quotename


    @quotename.setter
    def quotename(self, quotename):
        self._quotename = quotename


    @property
    def quoteauthor(self):
        return self._quoteauthor


    @quoteauthor.setter
    def quoteauthor(self, quoteauthor):
        self._quoteauthor = quoteauthor


    @property
    def opinion(self):
        return self._opinion


    @opinion.setter
    def opinion(self, opinion):
        self._opinion = opinion


    @property
    def rating(self):
        return self._rating


    @rating.setter
    def rating(self, rating):
        self._rating = rating


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
            "quotename": self.quotename,
            "quoteauthor": self.quoteauthor,
            "opinion": self.opinion,
            "rating": self.rating
        }


def initQuotes():
    with app.app_context():
        db.create_all()
        quotes = [
            Quote(quotename="Carpe Diem", quoteauthor="Horous Magic", opinion="Quote is very great!", rating=5),
            Quote(quotename="It is a great day", quoteauthor="Albert Dias", opinion="I know it is a great day", rating=4)
        ]
        for quote in quotes:
            try:
                quote.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {quote.quoteauthor}")