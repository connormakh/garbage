from app import db


class Company(db.Model):
    """This Class represents the company table, used for the user type company, in the admin portal"""

    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    contactNumber = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name, email, password, contactNumber):
        self.name = name
        self.password = password
        self.email = email
        self.contactNumber = contactNumber

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Company.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
