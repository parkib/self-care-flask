""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.String(255)) # change date to string
    _exercise = db.Column(db.JSON, nullable=True)
    _sleep = db.Column(db.JSON, nullable=True)
    _coins = db.Column(db.String, nullable=True)
    _role = db.Column(db.String(20), default="User", nullable=False)


    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, dob, exercise, sleep, coins, password="123qwerty", role="User"): #change place of dob
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self.set_password(password)
        self._dob = dob 
        self._role = role
        self._exercise = exercise
        self._sleep = sleep
        self._coins = coins

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        return self._dob 
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        return 9
        # today = date.today()
        # return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
   
    # hashmap is used to store python dictionary data, get rid of hashmap 
    
    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    def is_admin(self):
        return self._role == "Admin"
    
    
    
    @property
    def sleep(self):
        return self._sleep
    
    @sleep.setter
    def tracking(self, sleep):
        self._sleep = sleep
        
        
    @property
    def exercise(self):
        return self._exercise
    
    @exercise.setter
    def exercise(self, exercise):
        self._exercise = exercise
    
    @property
    def coins(self):
       return self._coins
     
    @coins.setter  
    def coins(self, coins):
        self._coins = coins
       

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
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            "age": self.age, 
            "coins": self.coins,
            "sleep": self.sleep,
            "exercise": self.exercise
            # "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="", coins="", sleep = "", exercise = ""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(coins) > 0:
            self.coins = coins
        if len(sleep) > 0:
            self.sleep = sleep
        if len(exercise) > 0:
            self.exercise = exercise
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
    def updatename(self, new_name=None):
        if new_name is not None:
            self.name = new_name
            db.session.commit()



"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Thomas Edison', uid='toby', password='123toby', dob=date(1847, 2, 11), role="Admin", sleep = "", exercise = "", coins = "0")
        u2 = User(name='Nicholas Tesla', uid='niko', password='123niko', dob=date(1856, 7, 10), sleep = "", exercise = "", coins = "0")
        u3 = User(name='Alexander Graham Bell', uid='lex', dob=date(1906, 12, 9), sleep = "", exercise = "", coins = "0" )
        u4 = User(name='Grace Hopper', uid='hop', password='123hop', dob=date(1906, 12, 9), sleep = "", exercise = "", coins = "0")
        users = [u1, u2, u3, u4]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
            