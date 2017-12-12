from flask import request, Blueprint
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


# TODO
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
