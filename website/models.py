from enum import unique
from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import ChoiceType
import enum

class UserRole(enum.Enum):
    admin = 1
    normal = 2


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    pseudo = db.Column(db.String(150))
    notes = db.relationship('Note')
    code_id = db.Column(db.Integer, db.ForeignKey('invite.id'))
    role = db.Column( ChoiceType(UserRole, impl= db.Integer()))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000)) #TODO changer limit ?
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    title = db.Column(db.String(60))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    notes = db.relationship('Note')

class Invite(db.Model):
    """Codes d'inivtations

    Args:
        db (_type_): id + code + creator + usages (int)
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(25))
    users = db.relationship('User')
    usages = db.Column(db.Integer)
    max = db.Column(db.Integer)
    creator = db.Column(db.String(42)) # Save pseudo as string for the logs