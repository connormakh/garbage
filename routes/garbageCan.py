from flask import request, Blueprint

from models.Company import Company
from models.CompanyRoutes import CompanyRoutes
from models.GarbageCanRequest import GarbageCanRequest
from models.GarbageStatus import GarbageStatus
from models.User import User
from models.GarbageCan import GarbageCan
from truckRouting.truckRouting import TruckRoutefinder
from util import common
from app import db
import json
import requests
import googlemaps

router = Blueprint('garbageCanRoutes', __name__)
gmaps = googlemaps.Client(key='AIzaSyD0q5ip6CbYFgzcha-Io-8lBM78PmgmslE')


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
                    id: company_id, req_id, latitude, longitude, volume
        """
    company_id = str(request.data.get('company_id', ''))
    req_id = str(request.data.get('req_id', ''))
    volume = str(request.data.get('volume', ''))
    latitude = str(request.data.get('latitude', ''))
    longitude = str(request.data.get('longitude', ''))

    if len(company_id) > 0 and Company.check_if_exists(company_id):

        can = GarbageCanRequest.objects(req_id=req_id).first()

        if can:
            can.delete()
            Company.add_garbage_can(company_id, req_id, volume, latitude, longitude)
            return common.to_json({}, "Can successfully added", 200)
        else:
            return common.to_json({}, "No such can addition request", 400)

    else:
        return common.to_json({}, "No such company", 400)


@router.route("/update", methods=['POST'])
def update_garbage_can_contents():
    """route: /garbage/update
                    POST: Update existing garbage bin details
                    params:
                         company_id, req_id, latitude, longitude, percentage_filled
            """
    company_id = str(request.data.get('company_id', ''))
    req_id = str(request.data.get('req_id', ''))
    percentage_filled = str(request.data.get('percentage_filled', ''))
    latitude = str(request.data.get('latitude', ''))
    longitude = str(request.data.get('longitude', ''))

    if company_id and req_id and percentage_filled and latitude and longitude and Company.check_if_exists(company_id):
        grbg_status = GarbageStatus()
        grbg_status.garbage_can_id = req_id
        grbg_status.completion = percentage_filled
        grbg_status.location = [latitude, longitude]
        grbg_status.save()
        return common.to_json({}, "Can update successfully submitted", 200)
    else:
        return common.to_json({}, "Can update is bad. Check your parameters.", 400)


@router.route("/statuses", methods=['GET'])
@User.token_required
def get_company_garbage_cans(current_user):
    """route: /garbage/<company_id>
                       GET: get company's garbage bins with their statuses
                       params:
                           id: company_id, req_id, latitude, longitude, percentage_filled
               """
    statuses = []
    for can in current_user.company.garbageCans:
        status = GarbageStatus.objects(garbage_can_id=can.name).order_by('-created_at').first()
        statuses.append(status)
    return common.to_json(statuses, "Cans successfully retrieved", 200)


@router.route("/route", methods=['GET'])
@User.token_required
def get_company_optimal_route(current_user):
    """route: /garbage/route
                           GET: get company's optimal route for garbage collection
                   """
    id = current_user.company.public_id

    # cans = GarbageStatus.objects(company_id=id, is_full=True)
    cans = []
    cans.append(GarbageStatus.create("1", "1", 1, [33.888630, 35.495480], 50, 50, True))
    cans.append(GarbageStatus.create("1", "22", 1, [33.911880, 36.0135800], 50, 50, True))
    cans.append(GarbageStatus.create("1", "222", 1, [33.271992, 35.203487], 50, 50, True))
    cans.append(GarbageStatus.create("1", "2222", 1, [34.123001, 35.651928], 50, 50, True))

    if len(cans) > 3:
        locations = []
        demands = []
        truck_capacity = current_user.company.truck_volume
        truck_count = current_user.company.truck_count
        for can in cans:
            locations.append([float(can.location[0]), float(can.location[1])])
            demands.append(can.volume)

        tr = TruckRoutefinder(locations, demands, 5, 500)
        routes = tr.find_route()
        if routes:
            CompanyRoutes.create(current_user.company.public_id, routes)
            return common.to_json(routes, "DONE", 200)
        else:
            return common.to_json({}, "No solution", 500)
    else:
        return common.to_json({}, "DONE", 400)