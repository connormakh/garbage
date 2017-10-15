from mongoengine import *


class GarbageStatus(Document):
    garbage_can_id = DecimalField(required=True)
    date = DateTimeField(required=True)
    completion = FloatField(required=True)

