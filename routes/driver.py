from app import db
from flask import request, Blueprint
from models.Driver import Driver
from models.DriverPickup import DriverPickup
from models.User import User
from util import common

router = Blueprint('driverRoutes', __name__)


@router.route("/new", methods=['POST'])
@User.token_required
def add_driver(current_user):
    """route: /driver/new
                POST: Add a driver for a company,
                 params: name, email, contact_number
        """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    contact_number = str(request.data.get('contact_number', ''))

    if name and email and contact_number:
        current_user.company.drivers.append(Driver(name, email, contact_number))
        db.session.commit()
        return common.to_json(current_user.json_serialize(), "Driver Added!", 200)
    else:
        return common.to_json({}, "Insufficient details for driver!", 400)


@router.route("/edit/<driver_id>", methods=['POST'])
@User.token_required
def edit_driver(current_user, driver_id):
    """route: /driver/edit
                    POST: Edit a driver for a company,
                     params: name, email, contact_number
                     All params are optional except for id
        """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    contact_number = str(request.data.get('contact_number', ''))

    if Driver.edit(driver_id, name, email, contact_number):
        return common.to_json({}, "Driver edited!", 200)
    else:
        return common.to_json({}, "Driver edit failed!", 400)


@router.route("/delete/<driver_id>", methods=['POST'])
@User.token_required
def delete_driver(current_user, driver_id):
    """route: /driver/delete
                    POST: Edit a driver for a company,
                     params: name, email, contact_number
                     All params are optional except for id
        """

    Driver.delete(driver_id)
    return common.to_json({}, "Driver deleted!", 200)


@router.route("/activity", methods=['GET'])
@User.token_required
def get_driver_activity(current_user):
    """route: /driver/activity
                    POST: Get driver activity for a company,
        """

    drivers = DriverPickup.get_driver_usage(current_user.company.public_id)

    return common.to_json(drivers, "Drivers retrieved!", 200)


