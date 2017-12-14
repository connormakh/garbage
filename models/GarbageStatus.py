from mongoengine import *
from datetime import datetime, timedelta


class GarbageStatus(Document):
    garbage_can_id = StringField(required=True)
    company_id = StringField(required=True)
    completion = FloatField(required=True)
    location = PointField()
    volume_filled = DecimalField()
    volume = DecimalField()
    created_at = DateTimeField(default=datetime.now())
    is_full = BooleanField(default=False)

    @staticmethod
    def create(can_id, company_id, completion, location, volume_filled, volume, isFull):
        can = GarbageStatus()
        can.garbage_can_id = can_id
        can.company_id = company_id
        can.completion = completion
        can.location = location
        can.volume_filled = volume_filled
        can.volume = volume
        can.is_full = isFull
        can.save()
        return can

    @staticmethod
    def get_consumption_graph(company_id):
        return GarbageStatus.objects.exec_js("""
        db.collection.aggregate(
   [
     {
       $group:
         {
           _id: { year: { $year: "$created_at" } },
           totalAmount: { $sum: $cond: {if :{$is_full}, then: $volume, else: 0}}
         }
     }
   ])
""")
