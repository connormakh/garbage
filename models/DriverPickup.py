from mongoengine import *
from datetime import datetime


class DriverPickup(Document):
    driver_id = StringField(required=True)
    driver_name = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())

    @staticmethod
    def create(driver_id, driver_name):
        can = DriverPickup()
        can.driver_id = driver_id
        can.driver_name = driver_name
        can.save()
        return can

    @staticmethod
    def get_driver_usage(company_id):
        return DriverPickup.objects.exec_js("""
            db.driver_pickup.aggregate(
       [
         {
           $group:
             {
               _id: { name: "$driver_name" },
               count: { $sum: 1}
             }
         }
       ])
    """, **{'company_id': company_id})