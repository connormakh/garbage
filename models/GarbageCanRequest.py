from mongoengine import *


class GarbageCanRequest(Document):
    company_id = DecimalField(required=True)
    date = DateTimeField(required=False)
    location = PointField()
    req_id = StringField()

    @staticmethod
    def create(company_id, latitude, longitude, req_id):
        can = GarbageCanRequest()
        can.company_id = company_id
        can.location = [latitude, longitude]
        can.req_id = req_id
        can.save()
