#local imports 
from flask import Flask
from marshmallow import  Schema,fields 
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma=Marshmallow()

db=SQLAlchemy()

class User(db.Model):
    
    """
    Users table
    """
    __tablename__='users'
    

    id=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    phone_number=db.Column(db.String(50),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    payments=db.relationship('Payment',backref=db.backref('users',lazy=True))
    
    def __init__(self,name,email,phone_number,age):
        self.name=name
        self.email=email
        self.phone_number=phone_number
        self.age=age

    #TODO: set iterable,better commenting

class UserSchema(ma.Schema):

    id=fields.String(required=True)
    name=fields.String(required=True)
    email=fields.String(required=True)
    phone_number=fields.String(required=True)
    age=fields.Integer()


class Payment(db.Model):
    """
    Payments table
    """
    __tablename__='payments'

    id=db.Column(db.String(50),primary_key=True)
    reference=db.Column(db.String(50),nullable=False)
    user_id=db.Column(db.String(50),db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    amount=db.Column(db.Float,nullable=False)
    def __init__(self, amount, reference,user_id):
      self.amount= amount
      self.reference= reference
      self.user_id= user_id

class PaymentSchema(ma.Schema):
    reference=fields.String(required=True)
    user_id=fields.String(required=True)
    amount=fields.Integer()