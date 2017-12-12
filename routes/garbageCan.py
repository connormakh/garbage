from flask import request, Blueprint

from models.Company import Company
from models.User import User
from models.GarbageCan import GarbageCan
from util import common
from app import db

router = Blueprint('garbageCanRoutes', __name__)


@router.route("/new", methods=['POST'])
@User.token_required
def add_garbage_can(current_user):
    """route: /garbage/new
            POST: Add a new garbage can for a user
            params:
                name(optional): string
    """
    can = GarbageCan(int(request.data.get('volume', '')), str(request.data.get('name', '')))
    current_user.company.garbageCans.append(can)
    db.session.commit()

    return common.to_json(can.json_serialize(), "Can successfully created", 200)


@router.route("/delete", methods=['POST'])
@User.token_required
def delete_garbage_can(current_user):
    """route: /garbage/delete
                POST: Delete a garbage can for a user
                params:
                    id: String
        """
    can_id = str(request.data('id', ''))
    if len(can_id) > 0:
        GarbageCan.delete_by_id(can_id)
        return common.to_json({}, "Can successfully deleted", 200)
    else:
        return common.to_json({}, "No such can", 400)


@router.route("/edit", methods=['POST'])
@User.token_required
def edit_garbage_can(current_user):
    """route: /garbage/edit
                POST: Delete a garbage can for a user
                params:
                    id: String
        """
    can_id = str(request.data('id', ''))
    if len(can_id) > 0:
        GarbageCan.delete_by_id(can_id)
        return common.to_json({}, "Can successfully deleted", 200)
    else:
        return common.to_json({}, "No such can", 400)


@router.route("/register", methods=['POST'])
def register_garbage_can():
    """route: /garbage/register
                POST: Register a company garbage bin
                params:
                    id: company_id, req_id
        """
    company_id = str(request.data('company_id', ''))
    req_id = str(request.data('req_id', ''))
    volume = str(request.data('volume', ''))
    latitude = str(request.data('latitude', ''))
    longitude = str(request.data('longitude', ''))

    if len(company_id) > 0 and Company.check_if_exists(company_id):
        Company.add_garbage_can(company_id, req_id, volume, latitude, longitude)
        return common.to_json({}, "Can successfully added", 200)
    else:
        return common.to_json({}, "No such company", 400)
