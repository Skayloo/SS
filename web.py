import csv
import datetime
import os
import random
import shutil
import sys
import time
import requests

import selenium
import PyQt5
from PyQt5 import QtCore
from selenium import webdriver

import Start

# Login:	gloger2003
# Password:	qDxPrakY


def check(day):
	power   = day['power']
	if not power: return False

	work_t  = day['time'].split('-')
	ts = float(work_t[0])
	tf = float(work_t[1])
	tn = float(f'{datetime.datetime.now().hour}.{datetime.datetime.now().minute}')
	if ts < tn < tf:
		return True
	return False


class AddToFriends(QtCore.QThread):
    def __init__(self, button, data, parent=None):
        super().__init__(parent=parent)

        self.button = button
        self.data = data
        self.get_sheet()

        shutil.rmtree('chrome-self.data', ignore_errors=True)


    def get_sheet(self):
        old_links = []

        try:
            f = open('FriendsAdded.csv', 'r')
            for row in csv.reader(f, delimiter=';'):
                old_links.append(row)
                print(row)
        except FileNotFoundError: pass

        self.f = open('FriendsAdded.csv', 'w', newline='')
        self.sheet = csv.writer(self.f, delimiter=';')
        self.sheet.writerows(old_links)



    def run(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-self.data-dir=chrome-self.data")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        chrome_options.add_argument("--remote-debugging-port=45447")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--log-level=3')
        # chrome_options.add_argument('--proxy-server=%s' % '64.154.38.86:8080')

        # Регаемся
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get('https://www.mql5.com/ru/auth_login')

        if '403 - Forbidden: Access is denied.' in self.driver.find_element_by_tag_name('body').text:
            while True:
                r = driver.refresh()
                if '403 - Forbidden: Access is denied.' in self.driver.find_element_by_tag_name('body').text: 
                    print('ОШИБКА 403!')
                    time.sleep(random.randint(int(a) for a in [self.data.serialDelay]))
                    if not self.data.isRUN_ADD: break
                else: break

        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_class_name('login').click()
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_id('Login').send_keys(self.data.login.split(':')[0])
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_id('Password').send_keys(self.data.login.split(':')[1])
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_id('loginSubmit').click()
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        

        all_ = 0 
        if self.data.isStartLastLink: 
            all_ = self.data.acceptLinks
        else: 
            all_ = 0
            self.data.acceptLinks = 0
        result = 0
        while True:
            k = 0
        
            ser = random.randint(*(int(a) for a in self.data.maxLinks.split('-')))
            while k < ser:
                if datetime.datetime.now().weekday() != self.data.linkDay[1]: 
                    self.data.linkDay[1] = datetime.datetime.now().weekday()
                    self.data.linkDay[0] = 0
                    self.data.acceptLinkDay[1] = 0
                if self.data.linkDay[0] >= self.data.linkDay[2] or int(self.data.acceptLinkDay[0]) <= int(self.data.acceptLinkDay[1]): break

                if check(self.data.days[str(datetime.datetime.now().weekday() + 1)]):
                    try: 
                        link = self.data.links[all_].replace(',', '') if self.data.links[all_].replace(',', '') != None else self.data.links[all_]
                        link = link.replace("'", '') if link.replace("'", '') != None else link
                        link = link.replace("'", '') if link.replace("'", '') != None else link 
                        link = link.replace("\"", '') if link.replace("\"", '') != None else link
                        link = link.replace("\"", '') if link.replace("\"", '') != None else link
                    except IndexError:
                        self.data.isRUN_ADD = False
                        self.f.close()
                        self.data.save()
                        self.driver.close()
                        self.button.setText('Добавить')
                        return

                    if not self.data.isRUN_ADD: break
                    
                    if str(link).find('https://www.mql5.com/') == -1:
                        for char in link:
                            if char == ' ': link = link.replace(char, '')
                        link = 'https://www.mql5.com/en/users/' + link
                        print(link)

                    result = self.addFriend(link)
                    if result == 1:
                        self.data.acceptLinks += 1
                        self.data.linkDay[0] = self.data.linkDay[0] + 1
                    if result == 3: break
                    if result == 2: time.sleep(10)
                
                    all_ += 1
                    k += result

                if not self.data.isRUN_ADD: break
                self.data.save()
                self.button.setText(f'{k}/{ser}')
                time.sleep(random.randint(int(self.data.delay[0]), int(self.data.delay[1])))
            

            self.button.setText('Zzz...')
            for k in range(random.randint(*(int(a) for a in self.data.serialDelay.split(':')))):
                time.sleep(1)
                if not self.data.isRUN_ADD:
                    self.f.close()
                    self.data.save()
                    self.driver.close()
                    self.button.setText('Добавить')
                    return

        self.data.isRUN_ADD = False
        self.f.close()
        self.data.save()
        self.driver.close()
        self.button.setText('Добавить')


    def addFriend(self, link):
        self.driver.get(link)
        if '403 - Forbidden: Access is denied.' in self.driver.find_element_by_tag_name('body').text:
            while True:
                self.driver.refresh()
                if '403 - Forbidden: Access is denied.' in self.driver.find_element_by_tag_name('body').text: 
                    print('ОШИБКА 403!')
                    time.sleep(time.sleep(random.randint(10, 100)))
                    if not self.data.isRUN_ADD: break
                else: break
            return

        if not self.data.isRUN_ADD: return 3
        try:
            try: rating = int(self.driver.find_element_by_class_name('profileMainDetails').find_elements_by_tag_name('a')[1].text)
            except ValueError: rating = int(self.driver.find_element_by_class_name('profileMainDetails').find_elements_by_tag_name('a')[2].text)
            except IndexError: rating = int(self.driver.find_element_by_class_name('profileMainDetails').find_elements_by_tag_name('a')[0].text)
            
            if not self.data.isRUN_ADD: return 3

            rat_min, rat_max = self.data.rating.split(':')
            print(rat_min, rat_max)

            if int(rat_min) <= rating <= int(rat_max):
                names = self.driver.find_elements_by_class_name('counterName')
                for k in names:
                    if ((((k.text == 'jobs' or k.text == 'job') or (k.text == 'работы' or k.text == 'работа' or k.text == 'работ'))                 and self.data.isCheckJobs) or 
                       (((k.text == 'products' or k.text == 'product') or (k.text == 'продукты' or k.text == 'продуктов' or k.text == 'продукт')    and self.data.isCheckProducts) or
                       ((k.text == 'signals' or k.text == 'signal') or (k.text == 'сигнала' or k.text == 'сигнал' or k.text == 'сигналы'))          and self.data.isCheckSignals)): return 1
                
                if not self.data.isRUN_ADD: return 3
                time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
                self.driver.find_element_by_css_selector("button.addToFriendsButton").click()
                self.data.acceptLinkDay[1] += 1
                self.sheet.writerow([link])
                if not self.data.isRUN_ADD: return 3

        except selenium.common.exceptions.NoSuchElementException: 
            print("Не найден")
            return 1
        return 1



class DelFromFriends(QtCore.QThread):
    def __init__(self, button, data, parent=None):
        super().__init__(parent=parent)

        self.button = button
        self.data = data

        shutil.rmtree('chrome-self.data', ignore_errors=True)


    def get_sheet(self):
        
        old_links = []

        try:
            f = open('FriendsDeleted.csv', 'r')
            for row in csv.reader(f, delimiter=';'):
                old_links.append(row)
        except FileNotFoundError: pass

        self.f = open('FriendsDeleted.csv', 'w', newline='')
        self.sheet = csv.writer(self.f, delimiter=';')
        self.sheet.writerows(old_links)


    def run(self):
        self.get_sheet()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-self.data-dir=chrome-self.data")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        chrome_options.add_argument("--remote-debugging-port=45447")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--log-level=3')
        # chrome_options.add_argument('--proxy-server=%s' % '64.154.38.86:8080')
        self.driver  = webdriver.Chrome(chrome_options=chrome_options)


        # Регаемся
        self.driver.get('https://www.mql5.com/ru/auth_login')
        if '403 - Forbidden: Access is denied.' in self.driver.find_element_by_tag_name('body').text:
            while True:
                self.driver.refresh()
                if '403 - Forbidden: Access is denied.' in self.driver.find_element_by_tag_name('body').text: 
                    print('ОШИБКА 403!')
                    time.sleep(time.sleep(random.randint(10, 100)))
                    if not self.data.isRUN_DEL:
                        self.data.isRUN_DEL = False
                        self.f.close()
                        self.data.save()
                        self.driver.close()
                        self.button.setText('Удалить')
                else: break

        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_class_name('login').click()
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_id('Login').send_keys(self.data.login.split(':')[0])
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_id('Password').send_keys(self.data.login.split(':')[1])
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        self.driver.find_element_by_id('loginSubmit').click()
        time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
        
        
        all_ = 0
        if self.data.isStartLastLink: 
            all_ = self.data.acceptLinks
        else: 
            all_ = 0
            self.data.acceptLinks = 0
            
        while True:
            ser = random.randint(*(int(a) for a in self.data.maxLinks.split('-')))
            
            k = 0
            while k < ser:

                if datetime.datetime.now().weekday() != self.data.linkDay[1]: 
                    self.data.linkDay[1] = datetime.datetime.now().weekday()
                    self.data.linkDay[0] = 0
                    self.data.acceptLinkDay[1] = 0
                
                if self.data.linkDay[0] >= self.data.linkDay[2] or int(self.data.acceptLinkDay[0]) <= int(self.data.acceptLinkDay[1]): break

                if not self.data.isRUN_DEL:
                    self.f.close()
                    self.data.save()
                    self.driver.close()
                    self.button.setText('Удалить')
                    return

                if check(self.data.days[str(datetime.datetime.now().weekday() + 1)]):
                    try:
                        if not self.data.isRUN_DEL: break
                        try:
                            link = self.data.links[all_].replace(',', '') if self.data.links[all_].replace(',', '') != None else self.data.links[all_]
                            link = link.replace("'", '') if link.replace("'", '') != None else link
                            link = link.replace("'", '') if link.replace("'", '') != None else link
                            link = link.replace("\"", '') if link.replace("\"", '') != None else link
                            link = link.replace("\"", '') if link.replace("\"", '') != None else link 
                        except IndexError:                                                
                            self.data.isRUN_DEL = False
                            self.f.close()
                            self.data.save()
                            self.driver.close()
                            self.button.setText('Удалить')
                            return

                        if not self.data.isRUN_DEL: break
                        
                        if str(link).find('https://www.mql5.com/') == -1:
                            for char in link:
                                if char == ' ': link = link.replace(char, '')
                            link = 'https://www.mql5.com/en/users/' + link
                        self.driver.get(link)

                        if not self.data.isRUN_DEL: break

                        try:
                            time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
                            self.driver.find_element_by_link_text('cancel').click()
                            time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
                            self.driver.switch_to.alert.accept()
                            self.data.acceptLinkDay[1] += 1
                            time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
                        except:
                            try:
                                time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
                                self.driver.find_element_by_link_text('отменить').click()
                                time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
                                self.driver.switch_to.alert.accept()
                                self.data.acceptLinkDay[1] += 1
                                time.sleep(random.randint(*(int(a) for a in self.data.doDelay.split(':'))))
                            except: pass
                        self.data.linkDay[0] = self.data.linkDay[0] + 1
                        self.sheet.writerow([link])
                        time.sleep(random.randint(int(self.data.delay[0]), int(self.data.delay[1])))
                    
                    except (selenium.common.exceptions.NoSuchElementException, AttributeError):
                        k += 1
                        all_ += 1
                        time.sleep(random.randint(int(self.data.delay[0]), int(self.data.delay[1])))
                    
                    all_ += 1
                    k += 1
                    self.button.setText(f'{k}/{ser}')
                    self.data.linkDay[0] = self.data.linkDay[0] + 1
                    self.data.acceptLinks += 1
                    self.data.save()
                
            self.button.setText('Zzz...')
            for k in range(random.randint(*(int(a) for a in self.data.serialDelay.split(':')))):
                time.sleep(1)
                if not self.data.isRUN_DEL:
                    self.f.close()
                    self.data.save()
                    self.driver.close()
                    self.button.setText('Удалить')
                    return
        
        self.data.isRUN_DEL = False
        self.f.close()
        self.data.save()
        self.driver.close()
        self.button.setText('Удалить')
