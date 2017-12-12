from flask import request, Blueprint

from mailer.Mailer import Mailer
from models.GarbageCanRequest import GarbageCanRequest
from models.User import User
from util import common

router = Blueprint('garbageCanRequestRoutes', __name__)


@router.route("/new", methods=['POST'])
@User.token_required
def add_garbage_request(current_user):
    """route: /garbage_request/new
                POST: Add a driver for a company,
                 params: name, email, contact_number
        """
    latitude = float(request.data.get('latitude', ''))
    longitude = float(request.data.get('longitude', ''))

    if latitude and longitude:
        GarbageCanRequest.create(company_id=current_user.company.id, latitude=latitude, longitude=longitude)
        req_id = current_user.company.public_id[1:8] + "0000" + len(current_user.company.garbageCans)
        mailer = Mailer()
        mailer.send_garbage_request(current_user.email, current_user.company.name, latitude, longitude, current_user.company.public_id, req_id)
        return common.to_json({}, "Request sent!", 200)
    else:
        return common.to_json({}, "Insufficient details for request!", 400)
