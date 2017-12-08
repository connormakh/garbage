from app import db
from instance.config import Config
from functools import wraps
from flask import request, jsonify
import uuid
import jwt
import json


class Driver(db.Model):
    """This Class represents the driver table.
        Driver indicates a truck driver for a company"""

    __tablename__ = 'driver'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    contact_number = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    # company = db.relationship("Company", backref='drivers') # one to many - parent must be defined in children

    def __init__(self, name, email, contact_number):
        self.name = name
        self.email = email
        self.contact_number = contact_number
        self.public_id = str(uuid.uuid4())

# INSTANCE-LEVEL METHODS

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# STATIC METHODS

    @staticmethod
    def edit(driver_id, name=None, email=None, contact_number=None):

        driver = Driver.query.filter_by(public_id=driver_id).first()

        if driver:
            if name:
                driver.name = name
            if email:
                driver.email = email
            if contact_number:
                driver.contact_number = contact_number
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def delete(driver_id):
        Driver.query.filter(Driver.public_id == driver_id).delete()
        db.session.commit()

# JSON SERIALIZATION METHODS

    def json_serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'contact_number': self.contact_number
        }

    @staticmethod
    def json_serialize_array(drivers):
        arr = []
        for driver in drivers:
            arr.append(driver.json_serialize())
        return arr

