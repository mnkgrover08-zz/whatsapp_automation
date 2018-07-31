from flask import jsonify, make_response
from flask import request
import requests
import flask_restful as restful
import sys, logging, json, re, os
from utility.logger import setup_logger
from configs.readconfig import configp
from sqlalchemy import desc
import time
from datetime import datetime
from add_new_contact_producer import Rabbit
import unittest
from appium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import uuid
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type


class WhatsAppNewContactListener(restful.Resource):

	def __init__(self):
		try:
			setup_logger('apilog', '/var/log/whatsapp_api/api.log')
			self.apilog = logging.getLogger('apilog')

		except Exception as e:
			self.apilog.error("SGLog:" + str("Unable to Initiate Logger"))
			self.apilog.error("SGLog:" + str(e), exc_info=True)

	def post(self):
		try:
			emulator_name = request.get_json().get('emulator_name', '')
			mobile_number = request.get_json().get('mobile_number', '')
			
			if emulator_name == '' or mobile_number == '':
				return make_response(jsonify({"status": "0", "message": "Insufficient Parameters"}), 422)

			mobile_format_validation = carrier._is_mobile(number_type(phonenumbers.parse(mobile_number)))

			if not mobile_format_validation:
				return make_response(jsonify({"status": "0", "message": "Mobile number not in International Indian Format. Ex: +91 XXXXX XXXXX"}), 400)
			
			final_message = json.dumps({"mobile_number":mobile_number,"emulator_name":emulator_name})

			add_contact_queue_name = configp.get('queue_name', 'add_contact')

			corr_id = Rabbit().msgproducer(add_contact_queue_name,final_message ,emulator_name)
			
			if corr_id:
				return make_response(jsonify({"status": "1", "message": "Singal received for Adding Contact", "corr_id": corr_id}), 200)
			else:
				return make_response(jsonify({"status": "0", "message": "Singal Failed", "corr_id": 0}), 400)
							
		except Exception as e:
			self.apilog.error("SGLog:"+ str(e))
			return make_response(jsonify({"status": "0", "message": "Exception Occured. Check Logs"}), 500)