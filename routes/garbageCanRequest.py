from flask import request, Blueprint

from mailer.Mailer import Mailer
from models.GarbageCanRequest import GarbageCanRequest
from models.User import User
from util import common
from random import randint


router = Blueprint('garbageCanRequestRoutes', __name__)


@router.route("/new", methods=['POST'])
@User.token_required
def add_garbage_request(current_user):
    """route: /garbage_request/new
                POST: Add a garbage request for a company,
                 params: latitude, longitude, location_details
        """
    latitude = float(request.data.get('latitude', ''))
    longitude = float(request.data.get('longitude', ''))
    location_details = request.data.get('location_details', '')

    if latitude and longitude:
        req_id = current_user.company.public_id[1:8] + str(randint(1, 999999))  + str(len(current_user.company.garbageCans))
        GarbageCanRequest.create(company_id=current_user.company.id, latitude=latitude, longitude=longitude, req_id=req_id)
        mailer = Mailer()
        mailer.send_garbage_request(current_user.email, current_user.company.name, latitude, longitude, current_user.company.public_id, req_id, location_details)
        return common.to_json({}, "Request sent!", 200)
    else:
        return common.to_json({}, "Insufficient details for request!", 400)
