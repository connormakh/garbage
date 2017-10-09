from app import db
from instance.config import Config
from functools import wraps
from flask import request, jsonify
import uuid
import jwt

class Company(db.Model):
    """This Class represents the company table, used for the user type company, in the admin portal"""

    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    contact_number = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name, email, password, contact_number):
        self.name = name
        self.password = password
        self.email = email
        self.contact_number  = contact_number
        self.public_id = str(uuid.uuid4())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_company(company_id):
        if id and id != -1:
            return Company.query.filter_by(id=company_id).first()
        else:
            return Company.query.all()

    def delete(self):
        db.session.delete(self)
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

    @staticmethod
    def authorize_by_name(name, password):
        current_user = Company.query.filter_by(name=name, password=password).first()

        if current_user:
            return str(jwt.encode({'public_id': current_user.public_id}, Config.SECRET, algorithm='HS256'))


    @staticmethod
    def authorize_by_email(email, password):
        current_user = Company.query.filter_by(email=email, password=password).first()

        if current_user:
            return str(jwt.encode({'public_id': current_user.public_id}, Config.SECRET, algorithm='HS256'))

    def json_serialize(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'contact_number': self.contact_number
        }
