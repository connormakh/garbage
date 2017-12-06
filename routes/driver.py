
from flask import request, Blueprint
from models.Company import Company
from models.User import User
from util import common
router = Blueprint('driverRoutes', __name__)


@router.route("<company_id>", methods=['GET'])
@User.token_required
def get_company(company_id):
    """route: /company/<company_id>
                POST: Edit company for user,
                 params: name, country, truck_count, truck_volume
        """
    company = Company.get_company(company_id=company_id, public=True)

    if company:
        return common.to_json(company.json_serialize(), "Company edited!", 200)
    else:
        return common.to_json({}, "Company not found!", 400)


@router.route("/edit", methods=['POST'])
@User.token_required
def edit_company(current_user):
    """route: /company/edit
            POST: Edit company for user,
             params: name, country, truck_count, truck_volume
    """
    name = str(request.data.get('name', ''))
    country = str(request.data.get('country', ''))
    truck_count = str(request.data.get('truck_count', ''))
    truck_volume = str(request.data.get('truck_volume', ''))

    if Company.edit_company_details(current_user.id, name, country, truck_count, truck_volume):
        return common.to_json({}, "Company edited!", 200)
    else:
        return common.to_json({}, "Company not found!", 400)

