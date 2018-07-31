import os
import unittest
from appium import webdriver
from time import sleep
import json
import sys
import re
import MySQLdb
from selenium.common.exceptions import NoSuchElementException


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', emulator_name= None,mobile_number=None,message_body=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.emulator_name = emulator_name
        self.mobile_number = mobile_number
        self.message_body = message_body

    @staticmethod
    def parametrize(testcase_klass, emulator_name= None,mobile_number=None,message_body=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, emulator_name= emulator_name,mobile_number=mobile_number,message_body=message_body))
        return suite

class WhatsAppSingleMessage(ParametrizedTestCase):
    "Class to run tests against the WhatsApp app"
    #def setUp(self):
    def setUp(self):
        "Setup for the test"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '9'
        desired_caps['deviceName'] = 'emulator-5554'
        # Returns abs path relative to this file and not cwd
        # desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'apps/whatsapp.apk'))
        desired_caps['appPackage'] = 'com.whatsapp'
        desired_caps['appActivity'] = '.Main'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.emulator_name = self.emulator_name
        self.mobile_number = self.mobile_number
        self.message_body = self.message_body
        # self.action = action

    def check_exists_by_xpath(self,xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_class_name(self,class_name):
        try:
            self.driver.find_elements_by_class_name(class_name)
        except NoSuchElementException:
            return False
        return True


    def tearDown(self):
        "Tear down the test"
        self.driver.quit()
    

    def runTest(self):
        self.test_single_mode()

    def test_single_mode(self):
        print "entered into whatsapp"
        final_whatsapp_message_broadcasted = self.message_body
        sleep(2)
        initiate_chat_button_xpath  = '//android.widget.ImageView[contains(@content-desc,"New chat") and contains(@resource-id,"fab")]'
        initiate_chat_button_xpath_status = self.check_exists_by_xpath(initiate_chat_button_xpath)
        if initiate_chat_button_xpath_status:
            initiate_chat_button_element = self.driver.find_element_by_xpath(initiate_chat_button_xpath)
            initiate_chat_button_element.click()
            sleep(2)
            search_contact_xpath = '//android.widget.TextView[contains(@resource-id,"menuitem_search") and contains(@content-desc,"Search")]'
            search_contact_xpath_status = self.check_exists_by_xpath(search_contact_xpath)
            if search_contact_xpath_status:
                search_contact_element = self.driver.find_element_by_xpath(search_contact_xpath)
                search_contact_element.click()
                sleep(2)
                search_text_box_xpath = '//android.widget.EditText[contains(@resource-id,"search_src_text")]'
                search_text_box_xpath_status = self.check_exists_by_xpath(search_text_box_xpath)
                if search_text_box_xpath_status:
                    search_text_box_element = self.driver.find_element_by_xpath(search_text_box_xpath)
                    search_text_box_element.click()
                    sleep(2)
                    search_text_box_element.send_keys(self.mobile_number)
                    sleep(2)
                    mobile_number = self.mobile_number
                    element_selected_chat_xpath = '//android.widget.TextView[contains(@resource-id,"contactpicker_row_name") and contains(@text,"{mobile_number}")]'.format(**locals())
                    element_selected_chat_xpath_status = self.check_exists_by_xpath(element_selected_chat_xpath)
                    if element_selected_chat_xpath_status:
                        element_selected_chat_element = self.driver.find_element_by_xpath(element_selected_chat_xpath)
                        element_selected_chat_element.click()
                        sleep(3)
                        message_body_xpath = '//android.widget.EditText[contains(@resource-id,"entry") and contains(@text,"Type a message")]'
                        message_body_xpath_status = self.check_exists_by_xpath(message_body_xpath)
                        if message_body_xpath_status:
                            message_body_element = self.driver.find_element_by_xpath(message_body_xpath)
                            message_body_element.click()
                            sleep(3)
                            message_body_element.send_keys(self.message_body)
                            send_element_xpath = '//android.widget.ImageButton[contains(@resource-id,"send") and contains(@content-desc,"Send")]'
                            send_element_status = self.check_exists_by_xpath(send_element_xpath)
                            if send_element_status:
                                send_element = self.driver.find_element_by_xpath(send_element_xpath)
                                send_element.click()
                                print "broadcast sent successfully"
                            else:
                                print " send element Not Found"
                            self.driver.back()
                            sleep(2)
                        else:
                            print "Message Body Element not found"
                    else:
                        print "Element chat selector not found"
                else:
                    print "search text box for typing not found"
            else:
                print "Search contact button icon not found"
        else:
            print "New Chat Icon/button not found"
 
#---START OF SCRIPT
#if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(WhatsAppSingleMessage(emulator_name,mobile_number,message_body))
    #unittest.TextTestRunner(verbosity=2).run(suite)