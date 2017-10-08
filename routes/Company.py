
from flask import request, jsonify, abort, Blueprint
from models import Company
router = Blueprint('companyRoutes', __name__)

@router.route("/new", methods=['POST'])
def companies():
    """route: /companies/
            POST: Create a new company, params name, email, password, contactNumber

    """
    name = str(request.data.get('name',''))
    email = str(request.data.get('email',''))
    password = str(request.data.get('password',''))
    contactNumber = str(request.data.get('contactNumber',''))

    if name and email and password and contactNumber:
        Company(name, email, password, contactNumber)


