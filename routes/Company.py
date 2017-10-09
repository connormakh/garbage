
from flask import request, Blueprint
from models.Company import Company
from util import common
router = Blueprint('companyRoutes', __name__)


@router.route("/new", methods=['POST'])
def add_company():
    """route: /companies/new
            POST: Create a new company, params name, email, password, contactNumber
    """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    contact_number = str(request.data.get('contact_number', ''))

    if name and email and password and contact_number:
        company = Company(name, email, password, contact_number)
        company.save()
        return common.to_json(company.json_serialize(), "Company successfully created!", 200)
    else:
        return common.to_json({}, "Required field missing", 400)


@router.route("/login", methods=['POST'])
def login_company():
    """route: /companies/login
            POST: login as a company [used through web portal]
            params: email/name, password
    """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))

    if name:
        token = Company.authorize_by_name(name, password)
    elif email:
        token = Company.authorize_by_email(email, password)
    else:
        return common.to_json({}, "Authorization failed!", 400)

    if token:
        return common.to_json({'token': token}, "Authorization success!", 200)
    else:
        return common.to_json({}, "Authorization failed!", 400)


@router.route("/<company_id>", methods=['GET'])
@Company.token_required
def get_companies(company_id):
    """route: /companies/:company_id
            GET: Get company by company_id
    """
    company = Company.get_company(company_id)

    if company:
        return common.to_json(company.json_serialize(), "Company successfully retrieved", 200)
    else:
        return common.to_json({}, "No such company", 400)