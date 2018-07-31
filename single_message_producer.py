import requests
import json
from configs.readconfig import configp
import logging
import pika
import uuid
import unittest
from appium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import sys, logging, json, re, os
from workers.whatsapp_single_message_worker import WhatsAppSingleMessage,ParametrizedTestCase

class Rabbit:

    def __init__(self):
        rhost = configp.get('rabbitmq', 'ip')
        username = configp.get('rabbitmq', 'username')
        password = configp.get('rabbitmq', 'password')
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(rhost,5672,'/',credentials)

        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)

        self.callback_queue = result.method.queue

    def msgproducer(self,queuename,message, emulatername, action):
    # Get the service resource
        try:
            routingkey = queuename+".*"
            exchange = queuename+".exchange"

            self.response = None
            self.corr_id = str(uuid.uuid4())

            res = self.channel.basic_publish(exchange=exchange,
                      routing_key=routingkey,
                      body=message,properties = pika.BasicProperties(reply_to = self.callback_queue,
                                             correlation_id = self.corr_id,headers={'emulator_name':emulatername, 'action': action}))

            if res:
                self.connection.close()
                return self.corr_id

            else:
                self.connection.close()
                return False
        except Exception as e:
            print e
            return False


    def msgworker(self, queuename):
        while 1:
            self.channel.basic_consume(self.callback, queue=queuename, no_ack=True)
            print "Waiting For Messages"
            self.channel.start_consuming()

    def callback(self,ch, method, properties, body):
        print body
        print properties
        if properties.headers['action'] == 'send_only':
            print type(body)
            body = eval(body)
            print body
            #body = json.loads(body)
            emulator_name = body['emulator_name']
            mobile_number = body['mobile_number']
            message_body = body['message_body']
            print message_body
            try:
                print "entered"
                #obj = WhatsAppSingleMessage().var_setup(emulator_name,mobile_number,message_body)
                suite = unittest.TestSuite()
                suite.addTest(ParametrizedTestCase.parametrize(WhatsAppSingleMessage, emulator_name=emulator_name,mobile_number=mobile_number,message_body=message_body))
                #suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=13))
                result = unittest.TextTestRunner(verbosity=2).run(suite)
                # unittest.TextTestRunner().run(suite)
                print "de-entetred"
            except Exception as e:
                print e

        elif properties.headers['action'] == 'create_and_send':
            print "Not handled"
        else:
            print "default handle"


        print(" [x] Received %r" % body)

    def main(self):
        
        global LOGGER

        FORMAT = '%(levelname)s: %(asctime)-15s: %(filename)s: %(funcName)s: %(module)s: %(message)s'
        logging.basicConfig(filename="/var/log/whatsapp_single_worker.log", level=logging.DEBUG, format=FORMAT)
        LOGGER = logging.getLogger("single_worker")
        single_message_queue_name = configp.get('queue_name', 'single_message')
        try:
            self.msgworker(single_message_queue_name)
        except Exception as e:
            LOGGER.error(e)

if __name__ == '__main__':
    rabbitInstance = Rabbit()
    rabbitInstance.main()