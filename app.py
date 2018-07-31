########### BASE IMPORTS ###############################
from flask import Flask, Response
import base64
import flask_restful as restful
from flasgger import Swagger


######### ENVIRONMENT CONFIGS ###########################
from configs.readconfig import configp

app = Flask(__name__)

apy = restful.Api(app)


from controllers.single_message import WhatsAppSingleMessage
apy.add_resource(WhatsAppSingleMessage, '/api/v0.1/send_single_message')


from controllers.broadcast_message import WhatsAppBroadcastMessage
apy.add_resource(WhatsAppBroadcastMessage, '/api/v0.1/send_broadcast_message')


from controllers.listen_message import WhatsAppMessageListener
apy.add_resource(WhatsAppMessageListener, '/api/v0.1/listen_new_message')


from controllers.add_new_contact import WhatsAppNewContactListener
apy.add_resource(WhatsAppNewContactListener, '/api/v0.1/add_new_contact')


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
    #app.run(debug=True, threaded=True)