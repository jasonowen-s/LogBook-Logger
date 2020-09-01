import os
import json
import datetime
from pytanggalmerah import TanggalMerah
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class logger(): 
    def askData(self):
        print('################################################')
        print('###              LOGBOOK LOGGER              ###')
        print('################################################')
        username = password = clock_in =  clock_out = weekend_activity = ''
        invalid_credentials = True
        while(invalid_credentials):
            print('\n>INPUT CREDENTIALS')
            username = input('  username           : ')
            password = input('  password           : ')
            with webdriver.Chrome(options=self.options) as driver:
                driver.get('https://industry.socs.binus.ac.id/learning-plan/auth/login')
                driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
                driver.find_element_by_xpath("//input[@name='password']").send_keys(password + Keys.ENTER)
                if(driver.title == 'SOCS - Learning Plan - Home'):
                    invalid_credentials = False
                    driver.get('https://industry.socs.binus.ac.id/learning-plan/logout')
                else:
                    print('\n  INVALID CREDENTIALS\n')
        print('\n>INPUT DEFAULT VALUES')
        while(len(clock_in) == 0):
            clock_in = input('  clock in           : ')
        while(len(clock_out) == 0):
            clock_out = input('  clock out          : ')
        while(len(weekend_activity) == 0):
            weekend_activity = input('  weekend activity   : ')
        data = {
            'username':username,
            'password':password,
            'clock_in':clock_in,
            'clock_out':clock_out,
            'weekend_activity':weekend_activity
        }
        with open(self.FILENAME, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('\n  data saved.\n')

    def fetchData(self):
        with open(self.FILENAME) as f:
            return json.load(f)

    def fill(self, username, password, clock_in, clock_out, activity, description):
        with webdriver.Chrome(options=self.options) as driver:
            try:
                print('\nlogging in...')
                driver.get('https://industry.socs.binus.ac.id/learning-plan/auth/login')
                driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
                driver.find_element_by_xpath("//input[@name='password']").send_keys(password + Keys.ENTER)
            except:
                print('\nlogging in failed!\n')
                return
            
            try:
                print('\nfilling log...')
                driver.get('https://industry.socs.binus.ac.id/learning-plan/student/log-book')
                driver.find_element_by_xpath("//input[@name='clock-in']").send_keys(clock_in)
                driver.find_element_by_xpath("//input[@name='clock-out']").send_keys(clock_out)
                driver.find_element_by_xpath("//input[@name='activity']").send_keys(activity)
                driver.find_element_by_xpath("//textarea[@name='description']").send_keys(description + Keys.TAB + Keys.ENTER)
            except:
                print('\nfilling log failed!\n')
                return
            
            try:
                print('\nchecking...')
                driver.get('https://industry.socs.binus.ac.id/learning-plan/student/log-book')
                result = (driver.find_elements_by_xpath("//div[@class='ui header']"))[1]
                header = (result.text[0:27] == 'You already filled activity')
                if(header):
                    tds = driver.find_elements_by_xpath("//td")
                    if((tds[1].text == clock_in) and (tds[3].text == clock_out) and (tds[5].text == activity) and (tds[7].text == description)):
                        print('\nLog successfully filled!\n')
                        return
            except:
                print("\nLogging failed!\n")

    def isWorkDay(self):
        t = TanggalMerah('./calendar.json')
        return not (t.check() or datetime.datetime.today().weekday()==5)

    def getDate(self):
        return datetime.datetime.today().strftime('%A,%e-%B-%Y')

    def getOffDayFormData(self):
        t = TanggalMerah('./calendar.json')
        t.check()
        activity = self.userData['weekend_activity'] if datetime.datetime.today().weekday()>4 else 'Libur '+t.get_event()[0]
        print('clock in    : -')
        print('clock out   : -')
        print('activity    : '+activity)
        print('description : -')
        return self.userData['username'], self.userData['password'], '-', '-', activity, '-'

    def getWorkDayFormData(self):
        print('clock in    : '+self.userData['clock_in'])
        print('clock out   : '+self.userData['clock_out'])
        weekdays_activity = input('activity    : ')
        description = input('description : ')
        return self.userData['username'], self.userData['password'], self.userData['clock_in'], self.userData['clock_out'], weekdays_activity, description

    def noDefault(self):
        if os.path.isfile('data.json'): return False
        return True

    def run(self):
        self.FILENAME = 'data.json'
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging']) #[optional] disables Selenium logging
        self.options.add_argument('--headless')                                     #[optional] hides Chrome window
        if self.noDefault() : self.askData()
        self.userData = self.fetchData()
        print('LOGBOOK FOR : '+self.getDate())
        username, password, clock_in, clock_out, activity, description = self.getWorkDayFormData() if self.isWorkDay() else self.getOffDayFormData()
        self.fill(username, password, clock_in, clock_out, activity, description)

if __name__ == '__main__':
    logger().run()