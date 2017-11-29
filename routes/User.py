
from flask import request, Blueprint
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

    if name and email and password and contact_number:
        verified = User.signup(name, email, password, contact_number)
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
        return common.to_json({}, "Authorization failed!", 400)


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
