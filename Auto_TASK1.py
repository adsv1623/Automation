import unittest         #  Ceated by  ADARSH RAJ . EMAIL: adarshrajsv@gmail.com    TASK 1

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging
import time
import subprocess
import os



class SiteCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''  
        logger configuration
        '''
        logging.basicConfig(filename='/home/adsv/Documents/Workspace/Automation/report.txt',
                            format='%(asctime)s: %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filemode='w')


        '''logger Object'''
        cls.logger = logging.getLogger()
        '''LEVEL setup'''
        cls.logger.setLevel(logging.DEBUG)

        cls.logger.debug('Process Start:DEBUG LEVEL')

        #Chrome driver
        cls.driver = webdriver.Chrome(executable_path=os.getcwd()+'/chromedriver')
        if cls.driver==None:
            cls.logger.error('Check Chrome Version ')
        else:
            cls.logger.info('Succefully Open Browser')
    

    def test_1_StatusCode(self):
        print('FETCHING-- Site\n')
        ###############################################  GETTING URL
        url='https://www.atg.party/'
        self.driver.get(url)

        #####################       PERFORMANCE OF LOADING PAGE
        navigationStart = self.driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = self.driver.execute_script("return window.performance.timing.responseStart")
        domComplete = self.driver.execute_script("return window.performance.timing.domComplete")
        
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete  - responseStart

        logging.info('backendPerformance: {}'.format(backendPerformance_calc))
        logging.info('frontendPerformance: {}'.format(frontendPerformance_calc))


        ######################     HTTP RESPONSE 
        HTTP_RC= '200' # HTTP response code == 200

        STATUS_CODE_LINE = subprocess.check_output(['tail', '-13','report.txt']).decode('utf-8')
        if HTTP_RC in STATUS_CODE_LINE:
            logging.info('HTTP response code == 200')
            print('HTTP response code == 200')
        else:
            logging.warn('RESPONSE STATUS: FAILED')

        
        

    def test_2_login(self):
        self.driver.find_element_by_link_text('Login').click()
        time.sleep(2)

        #############################  LOGIN CREDENTIAL
        email = 'wiz_saurabh@rediffmail.com'
        pwd   = 'Pass@123'

        self.driver.find_element(By.ID,'email').send_keys(email)
        self.driver.find_element(By.ID,'password').send_keys(pwd)
        submit =self.driver.find_elements_by_tag_name('button')[2]
        submit.click()
        logging.info('Loggin Successful')
        print('LOGIN SUCCESSFUL')
        time.sleep(5)
        

        #########################################   ARTICLE PUBLISH
        logging.info('SWITCHED TO PUBLISH/ARTICLE')
        url = 'https://www.atg.party/article'
        self.driver.get(url)

        Title = ' This For Automation '             #    Title of publish
        position =self.driver.find_element(By.ID,'title')
        position.send_keys(Title)

        desc = 'Post Automation With a Cover Image' #    DESCRIPTION
        position.send_keys(Keys.TAB)
        Loc_Frame =self.driver.switch_to_active_element()
        Loc_Frame.send_keys(desc)
        time.sleep(2)




    def test_3_post(self):      #  SUBMISSION PROCESS
        self.driver.find_element(By.ID,'article_pic').send_keys(os.getcwd()+'/img.jpg')
        time.sleep(10)
    
        self.driver.find_element(By.ID,'featurebutton').click()   #PUBLISH BUTTON
        time.sleep(5)
        plublished = self.driver.current_url()                    #PUBLISHED URL
        logging.info('Article:'+plublished)
        print('PUBLISHED AT:',plublished)
        

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.logger.info('Process End')            #END



if __name__ == "__main__":
    unittest.main()
