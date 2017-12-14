import os

from app import create_app
from coap import CoAPServer

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)
print("hiwefwef")
app.run(host='0.0.0.0', threaded=True, debug=True)
# CoAPServer.start_server()
# if __name__ == '__main__':
#     # pass

