import os
import unittest
from appium import webdriver
from time import sleep
import json
import sys
import re
import MySQLdb
from selenium.common.exceptions import NoSuchElementException


class BroadcastParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', emulator_name= None,mobile_number_list=None,message_body=None):
        super(BroadcastParametrizedTestCase, self).__init__(methodName)
        self.emulator_name = emulator_name
        self.mobile_number_list = mobile_number_list
        self.message_body = message_body

    @staticmethod
    def parametrize(testcase_klass, emulator_name= None,mobile_number_list=None,message_body=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, emulator_name= emulator_name,mobile_number_list=mobile_number_list,message_body=message_body))
        return suite

class WhatsAppBroadcastMessage(BroadcastParametrizedTestCase):
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
        self.mobile_number_list = self.mobile_number_list
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
        more_options_xpath = '//android.widget.ImageView[contains(@content-desc,"More options") and contains(@index,"1")]'
        more_options_status = self.check_exists_by_xpath(more_options_xpath)
        if more_options_status:
            more_options_element = self.driver.find_element_by_xpath(more_options_xpath)
            more_options_element.click()
            sleep(2)
            new_broadcast_xpath = '//android.widget.TextView[contains(@resource-id,"title") and contains(@text,"New broadcast")]'
            new_broadcast_status = self.check_exists_by_xpath(new_broadcast_xpath)
            if new_broadcast_status:
                new_broadcast_element = self.driver.find_element_by_xpath(new_broadcast_xpath)
                new_broadcast_element.click()
                sleep(2)
                mobile_numbers = self.mobile_number_list
                for mobile in mobile_numbers:
                    final_mobile = mobile
                    search_contact_xpath = '//android.widget.TextView[contains(@resource-id,"menuitem_search") and contains(@content-desc,"Search")]'
                    search_contact_status = self.check_exists_by_xpath(search_contact_xpath)
                    if search_contact_status:
                        search_contact_element = self.driver.find_element_by_xpath(search_contact_xpath)
                        search_contact_element.click()
                        sleep(1)
                        search_textbox_xpath = '//android.widget.EditText[contains(@resource-id,"search_src_text") and contains(@index,"0")]'
                        search_textbox_status = self.check_exists_by_xpath(search_textbox_xpath)
                        if search_textbox_status:
                            search_textbox_element = self.driver.find_element_by_xpath(search_textbox_xpath)
                            search_textbox_element.click()
                            sleep(1)
                            search_textbox_element.send_keys(final_mobile)
                            sleep(1)
                            select_chat_element_xpath = '//android.widget.TextView[contains(@resource-id,"chat_able_contacts_row_name") and contains(@text,"{final_mobile}")]'.format(**locals())
                            select_chat_element_status = self.check_exists_by_xpath(select_chat_element_xpath)
                            if select_chat_element_status:
                                select_chat_element = self.driver.find_element_by_xpath(select_chat_element_xpath)
                                select_chat_element.click()
                                print final_mobile
                                print "Contact added to Broadcast List"
                            else:
                                print "Contact Not Found by Search Result"
                            self.driver.back()
                            sleep(1)
                            self.driver.back()
                            sleep(1)
                        else:
                            print "search textbox element not found"
                    else:
                        print "Searching element Not Found"
                submit_button_xpath = '//android.widget.ImageButton[contains(@resource-id,"next_btn") and contains(@content-desc,"Create")]'
                submit_button_status = self.check_exists_by_xpath(submit_button_xpath)
                if submit_button_status:
                    submit_button_element = self.driver.find_element_by_xpath(submit_button_xpath)
                    submit_button_element.click()
                    sleep(2)
                    type_message_element_xpath = '//android.widget.EditText[contains(@resource-id,"entry") and contains(@text,"Type a message")]'
                    type_message_element_status = self.check_exists_by_xpath(type_message_element_xpath)
                    if type_message_element_status:
                        type_message_element = self.driver.find_element_by_xpath(type_message_element_xpath)
                        type_message_element.click()
                        sleep(1)
                        type_message_element.send_keys(final_whatsapp_message_broadcasted)
                        sleep(2)
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
                        print "Deleting Broadcast list"
                        more_options_xpath = '//android.widget.ImageView[contains(@content-desc,"More options") and contains(@index,"0")]'
                        more_options_status = self.check_exists_by_xpath(more_options_xpath)
                        if more_options_status:
                            more_options_element = self.driver.find_element_by_xpath(more_options_xpath)
                            more_options_element.click()
                            sleep(2)
                            broadcast_list_info_xpath = '//android.widget.TextView[contains(@resource-id,"title") and contains(@text,"Broadcast list info")]'
                            broadcast_list_info_status = self.check_exists_by_xpath(broadcast_list_info_xpath)
                            if broadcast_list_info_status:
                                broadcast_list_info = self.driver.find_element_by_xpath(broadcast_list_info_xpath)
                                broadcast_list_info.click()
                                sleep(2)
                                delete_broadcast_list_xpath = '//android.widget.TextView[contains(@resource-id,"exit_group_text") and contains(@text,"Delete broadcast list")]'
                                delete_broadcast_list_status = self.check_exists_by_xpath(delete_broadcast_list_xpath)
                                if delete_broadcast_list_status:
                                    delete_broadcast_list = self.driver.find_element_by_xpath(delete_broadcast_list_xpath)
                                    delete_broadcast_list.click()
                                    sleep(2)
                                    delete_broadcast_confirm_button_xpath = '//android.widget.Button[contains(@resource-id,"button1") and contains(@text,"DELETE")]'
                                    delete_broadcast_confirm_button_status = self.check_exists_by_xpath(delete_broadcast_confirm_button_xpath)
                                    if delete_broadcast_confirm_button_status:
                                        delete_broadcast_confirm_button = self.driver.find_element_by_xpath(delete_broadcast_confirm_button_xpath)
                                        delete_broadcast_confirm_button.click()
                                        sleep(1)
                                    else:
                                        print "Confirm Element not found for deleteing Broadcast"
                                    print "Broadcast Deleted Successfully"
                                else:
                                    print "Delete Broadcast button not Found"
                            else:
                                print "Broadcast Info element Not found"
                        else:
                            print "Unable to delete list More options not found"
                    else:
                        print "Broadcast Not Created Properly! Typing Element not Found!"
                else:
                    print "Submit Button Not Found"
            else:
                print "New Broadcast Element Not Found"
        else:
            print "More Options Button not Found"
