from app import db
from instance.config import Config
from functools import wraps
from flask import request, jsonify
import uuid
import jwt


class User(db.Model):
    """This Class represents the user table"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    contact_number = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    is_individual = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name, email, password, contact_number, is_individual=False):
        self.name = name
        self.password = password
        self.email = email
        self.contact_number = contact_number
        self.is_individual = is_individual
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
    def get_user(user_id):
        """Get a user record by user public id"""
        if id and id != -1:
            return User.query.filter_by(public_id=user_id).first()
        else:
            return User.query.all()



    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
                token = token[2:-1]  # strip from string chars

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, Config.SECRET, algorithms=['HS256'])
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except Exception as ex:
                print(ex)
                return jsonify({'message': 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated

    @staticmethod
    def authorize_by_name(name, password):
        current_user = User.query.filter_by(name=name, password=password).first()

        if current_user:
            return {'token': str(jwt.encode({'public_id': current_user.public_id}, Config.SECRET, algorithm='HS256')),
                    'user': current_user.json_serialize()}

    @staticmethod
    def authorize_by_email(email, password):
        current_user = User.query.filter_by(email=email, password=password).first()

        if current_user:
            return {'token': str(jwt.encode({'public_id': current_user.public_id}, Config.SECRET, algorithm='HS256')),
                    'user': current_user.json_serialize()}
    @staticmethod
    def signup(name, email, password, contact_number, company_name):
        current_user = User.query.filter_by(name=name, email=email).first()

        if current_user is None:
            user = User(name, email, password, contact_number, company_name)
            user.save()

            logged_in= User.query.filter_by(email=email, password=password).first()
            return {'token': str(jwt.encode({'public_id': logged_in.public_id}, Config.SECRET, algorithm='HS256')),
                    'user': logged_in.json_serialize()}

# JSON SERIALIZATION METHODS

    def json_serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'contact_number': self.contact_number,
            'type': 'Individual' if self.is_individual else 'Company'
        }
