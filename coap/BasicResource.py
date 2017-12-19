import aiocoap.resource as resource
import aiocoap

from models.Company import Company
from models.GarbageStatus import GarbageStatus


class BasicResource(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content. It is padded "\
                b"with numbers to be large enough to trigger blockwise "\
                b"transfer.\n")

    def set_content(self, content):
        self.content = content
        while len(self.content) <= 1024:
            self.content = self.content + b"0123456789\n"

    async def render_get(self, request):
        print("HELLO GET")
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        company_id = str(request.data.get('company_id', ''))
        req_id = str(request.data.get('req_id', ''))
        percentage_filled = str(request.data.get('percentage_filled', '0.0'))
        latitude = str(request.data.get('latitude', ''))
        longitude = str(request.data.get('longitude', ''))
        volume = str(request.data.get('volume', ''))
        predict_full = str(request.data.get('predict_full', '0'))
        print("check: " + str(Company.check_if_exists(company_id)))
        print("check: " + company_id)
        print(request.data)

        if company_id and req_id and percentage_filled and latitude and longitude and volume and Company.check_if_exists(
                company_id):
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
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
