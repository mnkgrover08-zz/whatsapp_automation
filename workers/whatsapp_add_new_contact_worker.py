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
    def __init__(self, methodName='runTest', emulator_name= None,mobile_number=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.emulator_name = emulator_name
        self.mobile_number = mobile_number

    @staticmethod
    def parametrize(testcase_klass, emulator_name= None,mobile_number=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, emulator_name= emulator_name,mobile_number=mobile_number))
        return suite

class WhatsAppAddNewContact(ParametrizedTestCase):
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
        desired_caps['appPackage'] = 'com.android.contacts'
        desired_caps['appActivity'] = '.activities.PeopleActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        #self.emulator_name = 'pixel_1'
        #self.mobile_number = '+91 78386 67436'
        #self.message_body = 'Hello There!'
        self.emulator_name = self.emulator_name
        self.mobile_number = self.mobile_number
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

    def check_exists_by_xpath_for_contacts(self,xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True


    def save_contact_with_mobile_as_name(self,mobile_number):
        first_name_xpath = '//android.widget.EditText[contains(@text,"First name") and contains(@index,"0")]'
        first_name_element_status = self.check_exists_by_xpath_for_contacts(first_name_xpath)

        phone_xpath = '//android.widget.EditText[contains(@text,"Phone") and contains(@index,"0")]'
        phone_element_status = self.check_exists_by_xpath_for_contacts(phone_xpath)
        print phone_element_status
        print first_name_element_status
        if first_name_element_status and phone_element_status:
            first_name_element = self.driver.find_element_by_xpath(first_name_xpath)
            first_name_element.click()
            first_name_element.send_keys(mobile_number)
            sleep(1)
            self.driver.back()
            sleep(1)
            phone_element = self.driver.find_element_by_xpath(phone_xpath)
            phone_element.click()
            phone_element.send_keys(mobile_number)
            save_contact_element_xpath = '//android.widget.Button[contains(@resource-id,"editor_menu_save_button") and contains(@text,"SAVE")]'
            save_contacts_element = self.driver.find_element_by_xpath(save_contact_element_xpath)
            save_contacts_element.click()
            sleep(1)
            return True
        else:
            print "First Name Or Phone not located in UI"
            return False
        return False


    def tearDown(self):
        "Tear down the test"
        self.driver.quit()
    

    def runTest(self):
        self.test_single_mode()

    def test_single_mode(self):
        print "entered into whatsapp"
        final_mobile = self.mobile_number
        print final_mobile
        sleep(1)
        search_contact_xpath = '//android.widget.TextView[contains(@resource-id,"menu_search") and contains(@index,"0")]'
        search_element_status = self.check_exists_by_xpath_for_contacts(search_contact_xpath)
        if search_element_status:
            search_element = self.driver.find_element_by_xpath(search_contact_xpath)
            search_element.click()
            sleep(1)
            search_text_element_xpath = '//android.widget.EditText[contains(@resource-id,"search_view") and contains(@text,"Search contacts")]'
            search_text_element_status = self.check_exists_by_xpath_for_contacts(search_text_element_xpath)
            if search_text_element_status:
                search_text_element = self.driver.find_element_by_xpath(search_text_element_xpath)
                search_text_element.click()
                sleep(1)
                search_text_element.send_keys(final_mobile)
                sleep(1)
                search_row_result_xpath = '//android.widget.TextView[contains(@resource-id,"cliv_name_textview") and contains(@text,"{final_mobile}")]'.format(**locals())
                print search_row_result_xpath
                search_row_result_status = self.check_exists_by_xpath_for_contacts(search_row_result_xpath)
                if search_row_result_status:
                    print "Contact Already Exists! No Need to ADD"
                    self.driver.back()
                    sleep(1)
                    self.driver.back()
                    sleep(1)
                else:
                    print "Contact Does not Exists! Adding in DB"
                    self.driver.back()
                    sleep(1)
                    self.driver.back()
                    sleep(1)
                    add_contact_button_xpath = '//android.widget.ImageButton[contains(@resource-id,"floating_action_button") and contains(@index,"0")]'

                    add_contact_button_status = self.check_exists_by_xpath_for_contacts(add_contact_button_xpath)

                    if add_contact_button_status:
                        add_contact_button = self.driver.find_element_by_xpath(add_contact_button_xpath)
                        add_contact_button.click()
                        sleep(1)
                        self.driver.back()
                        sleep(1)
                        new_contact_added_status = self.save_contact_with_mobile_as_name(final_mobile)
                        if new_contact_added_status:
                            print final_mobile + " added as Conatct in List"
                        else:
                            print "Unable to add Contact"
                        self.driver.back()
                    else:
                        print "Add Contact Button doesnot Exist"
            else:
                print "Search input box not Found"
        else:
            print "Search Click icon button not Found"


        print "Successfully Processed"
        print final_mobile
 
#---START OF SCRIPT
#if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(WhatsAppSingleMessage(emulator_name,mobile_number,message_body))
    #unittest.TextTestRunner(verbosity=2).run(suite)