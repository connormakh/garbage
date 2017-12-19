import asyncio

import aiocoap
import aiocoap.resource as resource

from coap.BasicResource import BasicResource
from coap.RegisterResource import RegisterResource


def start_server():
    print("COAP SERVER RUNNING")
    root = resource.Site()

    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('update',), BasicResource())
    root.add_resource(('register',), RegisterResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


