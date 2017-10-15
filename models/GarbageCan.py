from app import db
import uuid


class GarbageCan(db.Model):
    """This Class represents the garbage can table,
     used for reference for stored garbage cans per the user or company"""

    __tablename__ = 'garbageCan'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    volume = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    user = db.relationship("User", backref="garbageCans", primaryjoin="GarbageCan.user_id==User.id")

    def __init__(self, user_id, volume, name=""):
        self.name = name
        self.public_id = str(uuid.uuid4())
        self.user_id = user_id
        self.volume = volume

# INSTANCE-LEVEL METHODS

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# STATIC METHODS

    @staticmethod
    def get_garbage_can(can_id):
        if id and id != -1:
            return GarbageCan.query.filter_by(id=can_id).first()
        else:
            return GarbageCan.query.all()

    @staticmethod
    def get_user_garbage_cans(user_id):
        return GarbageCan.query.filter_by(user_id=user_id).all()



    @staticmethod
    def delete_by_id(can_id):
        GarbageCan.query.filter_by(public_id=can_id).delete()
        db.session.commit()


# JSON DESERIALIZATION METHODS

    def json_serialize(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'name': self.name
        }

    @staticmethod
    def json_serialize_list(l):
        json = []
        for i in l:
            json.append(i.json_deserialize())
        return json
