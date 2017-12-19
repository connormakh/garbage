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
from mongoengine.queryset.visitor import Q
import math

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
    latitude = (request.data.get('latitude', ''))
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
                         company_id, req_id, latitude, longitude, percentage_filled, predict_full, volume
            """
    company_id = str(request.data.get('company_id', ''))
    req_id = str(request.data.get('req_id', ''))
    percentage_filled = str(request.data.get('percentage_filled', '0.0'))
    latitude = str(request.data.get('latitude', ''))
    longitude = str(request.data.get('longitude', ''))
    volume = str(request.data.get('volume', ''))
    predict_full = str(request.data.get('predict_full', '0'))
    print("check: "+str(Company.check_if_exists(company_id)))
    print("check: "+company_id)
    print(request.data)


    if company_id and req_id and percentage_filled and latitude and longitude and volume and Company.check_if_exists(company_id):
        grbg_status = GarbageStatus()
        grbg_status.company_id = company_id
        grbg_status.garbage_can_id = req_id
        grbg_status.volume = volume
        grbg_status.completion = float(percentage_filled)
        if grbg_status.completion >= 0.8:
            grbg_status.is_full = True
        grbg_status.location = [float(latitude), float(longitude)]
        if predict_full == '1' and grbg_status.completion < 0.8:
            grbg_status.predict_full = True
        else:
            grbg_status.predict_full = False
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

    cans = GarbageStatus.objects.filter((Q(company_id=id) and Q(is_full=True)) or (Q(company_id=id) and Q(predict_full=True))).only('garbage_can_id').distinct('garbage_can_id')
    bins = []
    for id in cans:
        bin = GarbageStatus.objects(garbage_can_id=id, company_id=current_user.company.public_id).order_by('-created_by')
        if bin and (bin[len(bin) - 1].is_full or bin[len(bin) - 1].predict_full):
            bins.append(bin[len(bin) - 1])

    print(current_user.company.latitude)
    print(current_user.company.longitude)

    print(cans)
    if len(cans) > 2:
        locations = []
        demands = []
        truck_capacity = current_user.company.truck_volume
        truck_count = current_user.company.truck_count
        total_vol = 0
        trucks_to_be_added = 0
        for can in bins:
            print(can.volume)
        for can in bins:
            locations.append([float(can.location['coordinates'][0]), float(can.location['coordinates'][1])])
            demands.append(can.volume)
            total_vol += can.volume

        trucks_total_vol = truck_capacity * truck_count

        if trucks_total_vol < total_vol:
            trucks_to_be_added = math.ceil((total_vol - trucks_total_vol) / truck_capacity)

        print("locations: " + str(locations))
        print("demands: " + str(demands))
        print("tc: " + str(truck_count))
        print("trucks_to_be_added: " + str(trucks_to_be_added))
        print("truck_capacity: " + str(truck_capacity))
        tr = TruckRoutefinder(locations, demands, truck_count + trucks_to_be_added, truck_capacity)
        routes = tr.find_route()
        if routes:
            if trucks_to_be_added > 0:
                routes = routes[0:truck_count]
            CompanyRoutes.create(current_user.company.public_id, routes)
            return common.to_json(routes, "DONE", 200)
        else:
            return common.to_json({}, "No solution", 400)
    else:
        return common.to_json({}, "No cans", 400)


@router.route("/filled_stats/<type>", methods=['GET'])
@User.token_required
def get_filled_stats(current_user, type):
    """route: /garbage/filled_stats
        GET: get company filled stats
        query_params: type [y, m, d]

    """
    if type == "y":
        stats = GarbageStatus.get_filled_stats_by_year(current_user.company.public_id)
    if type == "m":
        stats = GarbageStatus.get_filled_stats_by_month(current_user.company.public_id)
    if type == "d":
        stats = GarbageStatus.get_filled_stats_by_day(current_user.company.public_id)

    return common.to_json(stats, "DONE", 200)


@router.route("/updates", methods=['GET'])
@User.token_required
def get_filled_stats_now(current_user):
    """route: /garbage/updates
        GET: get company garbage filled stats

    """
    stats = GarbageStatus.get_recent_bins(current_user.company.public_id)

    return common.to_json(stats, "DONE", 200)

