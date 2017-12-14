from mongoengine import *
from datetime import datetime, timedelta


class CompanyRoutes(Document):
    company_id = StringField(required=True)
    routes = ListField(required=True)
    created_at = DateTimeField(default=datetime.now())


    @staticmethod
    def create(company_id, routes):
        rt = CompanyRoutes()
        rt.company_id = company_id
        rt.routes = routes
        rt.save()
        return rt

