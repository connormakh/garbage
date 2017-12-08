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
        mailer = Mailer()
        mailer.send_garbage_request(current_user.email, current_user.company.name, latitude, longitude)
        return common.to_json({}, "Request sent!", 200)
    else:
        return common.to_json({}, "Insufficient details for request!", 400)
