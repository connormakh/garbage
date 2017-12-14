from app import db
from instance.config import Config
from functools import wraps
from flask import request, jsonify
import uuid
import jwt
import json

from models.GarbageCan import GarbageCan
from models.Driver import Driver


class Company(db.Model):
    """This Class represents the company table, used for the user type company, in the admin portal"""

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255))
    country = db.Column(db.String(255))
    contact_number = db.Column(db.String(255))
    truck_count = db.Column(db.Integer)
    truck_volume = db.Column(db.Integer)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    drivers = db.relationship('Driver', backref='company', lazy=True)
    garbageCans = db.relationship('GarbageCan', backref='company', lazy=True)


    def __init__(self, name):
        self.name = name
        self.public_id = str(uuid.uuid4())

# INSTANCE-LEVEL METHODS

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def edit(self, name=None, truck_count=None, truck_volume=None, country=None, latitude=None, longitude=None):
        if name:
            self.name = name
        if truck_count:
            self.truck_count = truck_count
        if truck_volume:
            self.truck_volume = truck_volume
        if country:
            self.country = country
        if latitude:
            self.latitude = latitude
        if longitude:
            self.longitude = longitude
        db.session.commit()

# STATIC METHODS

    @staticmethod
    def get_company(company_id, public=False):
        if public:
            if company_id and company_id != -1:
                return Company.query.filter_by(public_id=company_id).first()
            else:
                return Company.query.all()
        else:
            if company_id and company_id != -1:
                return Company.query.filter_by(id=company_id).first()
            else:
                return Company.query.all()


    @staticmethod
    def edit_company_details(company_id, name=None, truck_count=None, truck_volume=None, country=None):
        company = Company.query.filter_by(id=company_id).first()

        if company:
            if name:
                company.name = name
            if truck_count:
                company.truck_count = truck_count
            if truck_volume:
                company.truck_volume = truck_volume
            if country:
                company.country = country
            db.session.commit()
            return True
        return False

    @staticmethod
    def check_if_exists(company_id):
        company = Company.query.filter_by(public_id=company_id).first()

        if company:
            return True
        else:
            return False

    @staticmethod
    def add_garbage_can(company_id, req_id, volume, latitude, longitude):
        company = Company.query.filter_by(public_id=company_id).first()

        company.garbageCans.append(GarbageCan(volume, latitude, longitude, req_id))
        db.session.commit()


    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, Config.SECRET)
                current_user = Company.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated


# JSON SERIALIZATION METHODS

    def json_serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'country': self.country,
            'contact_number': self.contact_number,
            'drivers': Driver.json_serialize_array(self.drivers),
            'garbageCans': GarbageCan.json_serialize_list(self.garbageCans),
            'truck_count': self.truck_count,
            'truck_volume': self.truck_volume
        }
