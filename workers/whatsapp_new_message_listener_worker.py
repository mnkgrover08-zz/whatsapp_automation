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
    def __init__(self, methodName='runTest'):
        super(ParametrizedTestCase, self).__init__(methodName)

    @staticmethod
    def parametrize(testcase_klass):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name))
        return suite

class WhatsAppMessageListenr(ParametrizedTestCase):
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

    def check_exists_by_xpath(self,xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_xpath_in_element(self,element,xpath):
        try:
            element.find_element_by_xpath(xpath)
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
        sleep(5)
        m_user = configp.get('mysql', 'username')
        m_pass = configp.get('mysql', 'password')
        m_host = configp.get('mysql', 'host')
        m_db = configp.get('mysql', 'database')

        database = MySQLdb.connect (host=m_host, user = m_user, passwd = m_pass, db = m_db)
        database.set_character_set('utf8')
        cursor = database.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        badge_element_status = self.check_exists_by_xpath('//android.widget.TextView[contains(@resource-id,"badge")]')
        if badge_element_status:
            badge_element = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@resource-id,"badge")]')
            new_chats = badge_element.text
            if new_chats:
                new_chats = int(new_chats)
                if new_chats > 0:
                    initial_counter = 2
                    counter = initial_counter
                    for i in range(new_chats):
                        chat_element_xpath = '//android.widget.RelativeLayout[contains(@resource-id,"contact_row_container") and contains(@index, "{counter}")]'.format(**locals())
                        print chat_element_xpath
                        chat_element = self.driver.find_element_by_xpath(chat_element_xpath)
                        chat_element.click()
                        sleep(2)
                        single_chat_list_xpath = '//android.widget.ListView[contains(@resource-id,"list")]'
                        single_chat_list_status = self.check_exists_by_xpath(single_chat_list_xpath)
                        if single_chat_list_status:
                            single_chat_list = self.driver.find_element_by_xpath(single_chat_list_xpath)
                            total_view_classes_status = self.check_exists_by_class_name('android.view.ViewGroup')
                            if total_view_classes_status:
                                total_view_classes = single_chat_list.find_elements_by_class_name('android.view.ViewGroup')
                                count_total_view_classes = len(total_view_classes)
                                if count_total_view_classes > 0:
                                    # last_index_for_recent_message = count_total_view_classes 
                                    # print last_index_for_recent_message
                                    # last_message_xpath = '//android.view.ViewGroup[contains(@index, "{last_index_for_recent_message}")]'.format(**locals())
                                    # print last_message_xpath
                                    # last_message_status = self.check_exists_by_xpath(last_message_xpath)
                                    # print last_message_status
                                    last_message_container_element = total_view_classes[-1]
                                    if last_message_container_element:
                                        #last_message_container_element = single_chat_list.find_element_by_xpath(last_message_xpath)
                                        #last_message_container_element_status = self.check_exists_by_xpath('//android.widget.TextView[contains(@resource-id,"message_text")]')
                                        last_message_container_element_status = last_message_container_element
                                        if last_message_container_element_status:
                                            last_message = last_message_container_element.find_element_by_xpath('//android.widget.TextView[contains(@resource-id,"message_text")]')
                                            latest_message = str(last_message.text)
                                            print latest_message
                                            lower_latest_message = latest_message.lower()
                                            if lower_latest_message == 'start et':

                                                current_mobile_number_xpath = '//android.widget.TextView[contains(@resource-id,"conversation_contact_name")]'

                                                current_mobile_number_status = self.check_exists_by_xpath(current_mobile_number_xpath)                               

                                                if current_mobile_number_status:
                                                    
                                                    current_mobile_number = self.driver.find_element_by_xpath(current_mobile_number_xpath)

                                                    mobile_number = current_mobile_number.text
                                                    
                                                    mobile_number = current_mobile_number.text.encode('utf-8').strip()

                                                    print mobile_number

                                                    select_query = "SELECT id from subscribers WHERE mobile_number='{mobile_number}' LIMIT 1".format(**locals())
                                                    
                                                    cursor.execute(select_query)

                                                    select_row = cursor.fetchall()

                                                    if select_row:
                                                        select_id = select_row[0]
                                                    else:
                                                        select_id = 0

                                                    if select_id > 0:
                                                        query = """UPDATE subscribers SET active_status = 1 WHERE mobile_number = '{mobile_number}'""".format(**locals())
                                                        print query
                                                        cursor.execute(query)
                                                        database.commit()
                                                        print "Number Already Present subscribed as 1"
                                                    else:
                                                        query = """INSERT INTO subscribers(mobile_number) VALUES ('{mobile_number}')""".format(**locals())
                                                        print query
                                                        cursor.execute(query)
                                                        database.commit()
                                                        print "new mobile_number saved in DB"
                                                else:
                                                    print "Mobile Number Element not found"


                                            elif lower_latest_message == 'stop':


                                                current_mobile_number_xpath = '//android.widget.TextView[contains(@resource-id,"conversation_contact_name")]'

                                                current_mobile_number_status = self.check_exists_by_xpath(current_mobile_number_xpath)

                                                if current_mobile_number_status:
                                                    
                                                    current_mobile_number = self.driver.find_element_by_xpath(current_mobile_number_xpath)

                                                    mobile_number = current_mobile_number.text
                                                    
                                                    mobile_number = current_mobile_number.text.encode('utf-8').strip()

                                                    print mobile_number

                                                    select_query = "SELECT id from subscribers WHERE mobile_number='{mobile_number}' LIMIT 1".format(**locals())
                                                    
                                                    cursor.execute(select_query)

                                                    select_row = cursor.fetchall()

                                                    if select_row:
                                                        select_id = select_row[0]
                                                    else:
                                                        select_id = 0

                                                    if select_id > 0:
                                                        query = """UPDATE subscribers SET active_status = 0 WHERE mobile_number = '{mobile_number}'""".format(**locals())
                                                        print query
                                                        cursor.execute(query)
                                                        database.commit()
                                                        print "Subscription status updated to Unsubscribed"
                                                    else:
                                                        print "Subscriber Not found! Inserting first"
                                                        query = """INSERT INTO subscribers(mobile_number) VALUES ('{mobile_number}')""".format(**locals())
                                                        print query
                                                        cursor.execute(query)
                                                        database.commit()
                                                        print "Subscriber Saved Now Making Status Unsubscribed"
                                                        query = """UPDATE subscribers SET active_status = 0 WHERE mobile_number = '{mobile_number}'""".format(**locals())
                                                        print query
                                                        cursor.execute(query)
                                                        database.commit()
                                                        print "Subscription status updated to Unsubscribed"
                                                else:
                                                    print "Mobile Number Element not found"

                                                print "Stop Event Handled"

                                            else:
                                                print "ignoring random messages"
                                        else:
                                            print "Last Message Container Not Found"      
                                    else:
                                        print "Message not found in latest"

                                else:
                                    print "No chat Found in chat list"    

                            else:
                                print "No chat Found in chat list"   

                        else:
                            print "No Chat List Found For single Chat"
                else:
                    print "No new Chats count less than 1"
            else:
                print "No New Chats"
        else:
            print "No New Chats"
 
#---START OF SCRIPT
#if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(WhatsAppSingleMessage(emulator_name,mobile_number,message_body))
    #unittest.TextTestRunner(verbosity=2).run(suite)