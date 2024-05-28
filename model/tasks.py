from random import randrange
from datetime import datetime
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Task(db.Model):
    __tablename__ = 'tasks'  # table name is plural, class name is singular
    id = db.Column(db.Integer, primary_key=True)
    _taskname = db.Column(db.String(255), unique=False, nullable=False)
    _taskdeadline = db.Column(db.Date, unique=True, nullable=False)
    _taskdescription = db.Column(db.String(255), unique=False, nullable=False)
    _taskpriority = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, taskname, taskdeadline, taskdescription, taskpriority):
        self._taskname = taskname
        self._taskdeadline = datetime.strptime(taskdeadline, "%m/%d/%Y").date()
        self._taskdescription = taskdescription
        self._taskpriority = taskpriority

    @property
    def taskname(self):
        return self._taskname

    @taskname.setter
    def taskname(self, taskname):
        self._taskname = taskname

    @property
    def taskdeadline(self):
        return self._taskdeadline

    @taskdeadline.setter
    def taskdeadline(self, taskdeadline):
        self._taskdeadline = datetime.strptime(taskdeadline, "%m/%d/%Y").date()

    @property
    def taskdescription(self):
        return self._taskdescription

    @taskdescription.setter
    def taskdescription(self, taskdescription):
        self._taskdescription = taskdescription

    @property
    def taskpriority(self):
        return self._taskpriority

    @taskpriority.setter
    def taskpriority(self, taskpriority):
        self._taskpriority = taskpriority

    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "id": self.id,
            "taskname": self.taskname,
            "taskdeadline": self.taskdeadline.strftime("%m/%d/%Y"),
            "taskdescription": self.taskdescription,
            "taskpriority": self.taskpriority,
        }

def initTasks():
    with app.app_context():
        db.create_all()
        tasks = [
            Task(taskname="Finish studying for math test", taskdeadline="2024-06-23", taskdescription="The topics on the test are parabolic motion and parametric equations.", taskpriority="high"),
            Task(taskname="Finish stuyding for science exam", taskdeadline="2024-05-18", taskdescription="The test will cover everything from the past year.", taskpriority="high"),
            Task(taskname="Go to the grocery store", taskdeadline="2024-07-28", taskdescription="I need to buy mangoes, yogurt and honey", taskpriority="low")
        ]
        for task in tasks:
            try:
                task.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Error adding task: {task.taskname}")

