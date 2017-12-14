
from flask import request, Blueprint

from mailer.Mailer import Mailer
from models.CompanyRoutes import CompanyRoutes
from models.Driver import Driver
from models.GarbageStatus import GarbageStatus
from models.User import User
from util import common
router = Blueprint('userRoutes', __name__)


@router.route("/new", methods=['POST'])
def add_user():
    """route: /user/new
            POST: Create a new user,
             params: name, email, password, contactNumber
    """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    contact_number = str(request.data.get('contact_number', ''))

    if name and email and password and contact_number:
        user = User(name, email, password, contact_number)
        user.save()
        return common.to_json(user.json_serialize(), "User successfully created!", 200)
    else:
        return common.to_json({}, "Required field missing", 400)


@router.route("/signup", methods=['POST'])
def signup_user():
    """route: /user/signup
            POST: Create a new user,
             params: name, email, password, contactNumber
    """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    contact_number = str(request.data.get('contact_number', ''))
    company_name = str(request.data.get('company_name', ''))

    if name and email and password and contact_number:
        verified = User.signup(name, email, password, contact_number, company_name)
        if verified:
            return common.to_json({'token': verified['token'], 'user': verified['user']}, message="Signup success!",
                                  code=200)
        else:
            return common.to_json({}, "User already exists", 400)
    return common.to_json({}, "Required field missing", 400)


@router.route("/login", methods=['POST'])
def login_user():
    """route: /user/login
            POST: login as a user
            params:
                email/name, password
    """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))

    if name:
        token = User.authorize_by_name(name, password)
    elif email:
        token = User.authorize_by_email(email, password)
    else:
        return common.to_json({}, "Authorization failed!", 400)

    if token:
        print(token)
        return common.to_json({'token': token['token'], 'user': token['user']}, message="Authorization success!", code=200)
        #return token
    else:
        return common.to_json({}, "Authorization failed!2", 400)


@router.route("/<user_id>", methods=['GET'])
@User.token_required
def get_users(user_id, current_user):
    """route: /user/:user_id
            GET: Get user by public id
    """
    user = User.get_user(user_id)

    if user:
        return common.to_json(user.json_serialize(), "User successfully retrieved", 200)
    else:
        return common.to_json({}, "No such User", 400)


@router.route("/collection/graph", methods=['GET'])
@User.token_required
def get_collection_graph(current_user):
    """route: /user/collection/graph
                GET: Get user garbage collection statistics
                query params: type [y, m , d]
        """
    if type:
        result = GarbageStatus.get_consumption_graph(current_user.company.public_id)
        return common.to_json(result, "all good", 200)

    else:
        return common.to_json({}, "No param givenr", 400)


@router.route("/collection/send", methods=['POST'])
@User.token_required
def send_driver_route(current_user):
    """route: /user/collection/send
                    POST: Send driver to pick up garbage
                    params: driver_id, route_id

            """
    driver_id = str(request.data.get('driver_id', ''))
    route_id = int(request.data.get('route_id', 0))
    driver = Driver.query.filter_by(public_id=driver_id).first()
    crt = CompanyRoutes.objects(company_id=current_user.company.public_id).order_by('-created_at').first()
    if crt:
        if len(crt.routes) > route_id:
            mailer = Mailer()
            mailer.send_routing_message(current_user.email, driver.email, current_user.company.name, crt.routes[route_id])
            return common.to_json({}, "DONE", 200)
        else:
            return common.to_json({}, "Bad route id", 400)
    else:
        return common.to_json({}, "No such routes", 400)
