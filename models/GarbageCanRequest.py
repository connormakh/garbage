from mongoengine import *


class GarbageCanRequest(Document):
    company_id = DecimalField(required=True)
    date = DateTimeField(required=False)
    location = PointField()

    @staticmethod
    def create(company_id, latitude, longitude):
        can = GarbageCanRequest()
        can.company_id = company_id
        can.location = [latitude, longitude]
        can.save()
