import aiocoap.resource as resource
import aiocoap

from models.Company import Company
from models.GarbageCanRequest import GarbageCanRequest


class RegisterResource(resource.Resource):
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
        print('PUT payload: %s' % request.payload)
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

        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
