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
from new_message_listener_producer import Rabbit
import unittest
from appium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import uuid
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type


class WhatsAppMessageListener(restful.Resource):

	def __init__(self):
		try:
			setup_logger('apilog', '/var/log/whatsapp_api/api.log')
			self.apilog = logging.getLogger('apilog')

		except Exception as e:
			self.apilog.error("SGLog:" + str("Unable to Initiate Logger"))
			self.apilog.error("SGLog:" + str(e), exc_info=True)

	def post(self):
		try:
			special_code = request.get_json().get('special_code', '')
			if special_code == '':
				return make_response(jsonify({"status": "0", "message": "Insufficient Parameters"}), 422)

			if special_code != 'e3gi8d2i8d2382@@#':
				return make_response(jsonify({"status": "0", "message": "Special Code needs to be passed to listen message"}), 400)

			listen_message_queue_name = configp.get('queue_name', 'listen_message')

			corr_id = Rabbit().msgproducer(listen_message_queue_name)
			
			if corr_id:
				return make_response(jsonify({"status": "1", "message": "Singal received for listening message", "corr_id": corr_id}), 200)
			else:
				return make_response(jsonify({"status": "0", "message": "Singal Failed", "corr_id": 0}), 400)

		except Exception as e:
			self.apilog.error("SGLog:"+ str(e))
			return make_response(jsonify({"status": "0", "message": "Exception Occured. Check Logs"}), 500)