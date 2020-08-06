import datetime
import json
import os
import shutil
import sys
import time
from threading import Thread

import PyQt5
import selenium
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont
# from selenium import webdriver

import web

# Login:	gloger2003
# Password:	qDxPrakY


class AddThread(QThread):
    def __init__(self, data, button, parent=None):
        super().__init__(parent=parent)
        self.button = button
        self.data = data
        self.setTerminationEnabled(True)

    def run(self):
        for k in range(10):
            if not self.data.isRUN_ADD:
                break
            self.button.setText(str(k))
            time.sleep(1)





class Data:
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        self.isRUN_ADD = False
        self.isRUN_DEL = False

        self.isCheckJobs     = True
        self.isCheckProducts = True
        self.isCheckSignals  = True
        self.isStartLastLink = False

        self.doDelay = ''

        self.linkDay = [0, 0, 0]
        
        self.days = {
            '1': {'power': False, 'time': '', 'acceptLinkDay': ''}, 
            '2': {'power': False, 'time': '', 'acceptLinkDay': ''}, 
            '3': {'power': False, 'time': '', 'acceptLinkDay': ''}, 
            '4': {'power': False, 'time': '', 'acceptLinkDay': ''}, 
            '5': {'power': False, 'time': '', 'acceptLinkDay': ''}, 
            '6': {'power': False, 'time': '', 'acceptLinkDay': ''}, 
            '7': {'power': False, 'time': '', 'acceptLinkDay': ''}
            }

        self.acceptLinkDay = [0, 0]
        self.maxLinks    = 0
        self.delay       = (0, 0)
        self.links       = []
        self.acceptLinks = 0
        self.login       = ''
        self.rating      = ''
        self.serialDelay = ''
        self.openData()


    def openData(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(fp=f, parse_int=int())
                self.isCheckJobs     = bool(data['isCheckJobs'])
                self.isCheckProducts = bool(data['isCheckProducts'])
                self.isCheckSignals  = bool(data['isCheckSignals']) 
                self.isStartLastLink = bool(data['isStartedLast'])
                
                self.days        = data['days']
                self.maxLinks    = data['maxLinks']
                try: self.delay    = [data['delay'][0], data['delay'][1]]
                except: self.delay = ''
                self.links       = data['links']
                self.acceptLinks = data['acceptLinks']
                self.login       = data['login']
                self.rating      = data['rating']
                self.serialDelay = data['serialDelay']
                self.doDelay     = data['doDelay']
                self.linkDay[2]  = data['linkDay']
                self.acceptLinkDay = data['acceptLinkDay']
        except FileNotFoundError: pass


    def save(self):
        self.isCheckJobs     = self.frame.isCheckJobs.isChecked()
        self.isCheckProducts  = self.frame.isCheckProducts.isChecked()
        self.isCheckSignals  = self.frame.isCheckSignals.isChecked()
        self.isStartLastLink = self.frame.isStartLastLink.isChecked()
        

        self.maxLinks    = self.frame.maxLinksLine.text()
        self.delay       = [a for a in self.frame.delayLine.text().split(':')]
        print(self.frame.linkEdit.toPlainText())
        self.links       = self.frame.linkEdit.toPlainText().splitlines()

        # "log1\nlog2\n".splitlines() => ['log1', 'log2']


        self.login       = self.frame.logLine.text()
        self.serialDelay = self.frame.delaySerialLine.text()
        self.doDelay     = self.frame.doDelayLine.text()
        self.acceptLinkDay[0] = int(self.frame.acceptLinkDayLine.text())
        try: self.linkDay[2]    = int(self.frame.linkDayLine.text())
        except: self.linkDay[2] = 0
        self.rating      = self.frame.maxRatingLine.text()
        
        data = {
            'isCheckJobs':      self.isCheckJobs,
            'isCheckProducts':  self.isCheckProducts,
            'isCheckSignals':   self.isCheckSignals,
            'isStartedLast':    self.isStartLastLink,
            'links':            self.links,
            'acceptLinks':      self.acceptLinks,
            'maxLinks':         self.maxLinks,
            'delay':            self.delay,
            'serialDelay':      self.serialDelay,
            'login':            self.login,
            'rating':           self.rating,
            'days':             self.days,
            'doDelay':          self.doDelay,
            'linkDay':          self.linkDay[2],
            'acceptLinkDay':    self.acceptLinkDay
            }

        json.dump(fp=open('data.json', 'w'), obj=data, indent=2)
        print('Сохранил')


    def setDay(self, number, power, time, acceptLinkDay):
        self.days[number] = {
            'power':  power,
            'time':   time,
            'acceptLinkDay': acceptLinkDay
        }
        self.save()
        print('День установлен')
    


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.frame = QtWidgets.QFrame(self)
        self.data = Data(self)
        self.switchMode = False


        self.linkEdit = QtWidgets.QTextEdit(self.frame)
        self.linkEdit.setPlaceholderText('ссылка1\nссылка2\n...')
        self.linkEdit.setToolTip('Вставьте ссылки (Если между ссылками будет запятая или ковычки, скрипт уберёт ее), пример без запятой:\nссылка1\nссылка2\n...\n\nПример с запятой:\nссылка1,\nссылка2,\n...')
        self.linkEdit.setFont(QFont("oblique", 13))
        self.linkEdit.setWordWrapMode(False)
        self.linkEdit.move(10, 10)
        self.linkEdit.resize(400, 370)
        for line in self.data.links:
            self.linkEdit.append(line)
        

        self.logLine = QtWidgets.QLineEdit(self.frame)
        self.logLine.setPlaceholderText('login:password')
        self.logLine.setToolTip('Введите логин и пароль в виде логин:пароль, пример:\nNike232:888X999')
        self.logLine.setFont(QFont("oblique", 15))
        self.logLine.resize(400, 30)
        self.logLine.move(10, 390)
        self.logLine.setText(self.data.login)


        self.isCheckJobs = QtWidgets.QCheckBox(self.frame)
        self.isCheckJobs.setText('Проверять на работы')
        self.isCheckJobs.move(420, 10)
        self.isCheckJobs.setChecked(self.data.isCheckJobs)

        self.isCheckProducts = QtWidgets.QCheckBox(self.frame)
        self.isCheckProducts.setText('Проверять на продукты')
        self.isCheckProducts.move(420, 30)
        self.isCheckProducts.setChecked(self.data.isCheckProducts)

        self.isCheckSignals = QtWidgets.QCheckBox(self.frame)
        self.isCheckSignals.setText('Проверять на сигналы')
        self.isCheckSignals.move(420, 50)
        self.isCheckSignals.setChecked(self.data.isCheckSignals)



        self.maxLinksLine = QtWidgets.QLineEdit(self.frame)
        self.maxLinksLine.move(420, 80)
        self.maxLinksLine.resize(100, 20)
        self.maxLinksLine.setPlaceholderText("от-до")
        self.maxLinksLine.setToolTip('Интервал кол-ва ссылок для одной серии, пример:\n10-100')
        self.maxLinksLine.setText(str(self.data.maxLinks))


        self.maxRatingLine = QtWidgets.QLineEdit(self.frame)
        self.maxRatingLine.move(530, 80)
        self.maxRatingLine.resize(100, 20)
        self.maxRatingLine.setPlaceholderText('от:до')
        self.maxRatingLine.setToolTip('Мин:Макс рэйтинг, пример:\n500:10000')
        self.maxRatingLine.setText(self.data.rating)

        self.delaySerialLine = QtWidgets.QLineEdit(self.frame)
        self.delaySerialLine.move(420, 110)
        self.delaySerialLine.resize(100, 20)
        self.delaySerialLine.setPlaceholderText('от:до')
        self.delaySerialLine.setToolTip('Задержка между сериями в секундах от:до, пример:\n1:10')
        try: self.delaySerialLine.setText(self.data.serialDelay)
        except: pass

        self.delayLine = QtWidgets.QLineEdit(self.frame)
        self.delayLine.move(530, 110)
        self.delayLine.resize(100, 20)
        self.delayLine.setPlaceholderText('от:до')
        self.delayLine.setToolTip('Задержка между загрузкой профилей в секундах от:до, пример:\n1:10')
        try: self.delayLine.setText(f'{self.data.delay[0]}:{self.data.delay[1]}')
        except: pass

        self.daysBox = QtWidgets.QComboBox(self.frame)
        self.daysBox.move(420, 170)
        self.daysBox.setToolTip('Выберите день недели (Пн - 1, Вт - 2, ...)')
        self.daysBox.addItems(['1', '2', '3', '4', '5', '6', '7'])
        self.daysBox.setCurrentText(str(datetime.datetime.now().weekday() + 1))
        
        self.isDayWorked = QtWidgets.QCheckBox(self.frame)
        self.isDayWorked.move(460, 171)
        self.isDayWorked.setText("Работать в этот день")


        self.timeWorkLine = QtWidgets.QLineEdit(self.frame)
        self.timeWorkLine.move(420, 200)
        self.timeWorkLine.resize(140, 20)
        self.timeWorkLine.setFont(QFont("oblique", 10))
        self.timeWorkLine.setPlaceholderText('начало(час.мин)-конец(час.мин)')
        self.timeWorkLine.setToolTip("Запишите время работы в виде начало(час.мин)-конец(час.мин), пример:\n10.00-20.00")



        self.acceptLinkDayLine = QtWidgets.QLineEdit(self.frame)
        self.acceptLinkDayLine.move(570, 200)
        self.acceptLinkDayLine.resize(60, 20)
        self.acceptLinkDayLine.setPlaceholderText("nMax")
        self.acceptLinkDayLine.setToolTip('Максимальное кол-во удачных ссылок за день, пример:\n100')
        self.acceptLinkDayLine.setText(str(self.data.acceptLinkDay[0]))


        self.writeDay(self.daysBox.currentText())
        self.daysBox.currentTextChanged.connect(lambda: self.writeDay(self.daysBox.currentText()))




        self.linkDayLine = QtWidgets.QLineEdit(self.frame)
        self.linkDayLine.move(421, 140)
        self.linkDayLine.resize(100, 20)
        self.linkDayLine.setPlaceholderText("nMax")
        self.linkDayLine.setToolTip('Максимальное кол-во ссылок за день, пример:\n100')
        self.linkDayLine.setText(str(self.data.linkDay[2]))



        self.doDelayLine = QtWidgets.QLineEdit(self.frame)
        self.doDelayLine.move(530, 140)
        self.doDelayLine.resize(100, 20)
        self.doDelayLine.setPlaceholderText("от:до")
        self.doDelayLine.setToolTip('Задержка между действиями в секундах от:до, пример:\n1:5')
        self.doDelayLine.setText(str(self.data.doDelay))


        self.setDayButton = QtWidgets.QPushButton(self.frame)
        self.setDayButton.move(420, 230)
        self.setDayButton.resize(210, 30)
        self.setDayButton.setText('Задать расписание на день')
        self.setDayButton.clicked.connect(lambda: self.data.setDay( self.daysBox.currentText(), 
                                                                    self.isDayWorked.isChecked(), 
                                                                    self.timeWorkLine.text(),
                                                                    self.acceptLinkDayLine.text()))


        self.returnAcceptLinkButton = QtWidgets.QPushButton(self.frame)
        self.returnAcceptLinkButton.move(420, 270)
        self.returnAcceptLinkButton.resize(210, 30)
        self.returnAcceptLinkButton.setToolTip('Если программа будет стоять, попробуйте сбросить кол-во удачных ссылок')
        self.returnAcceptLinkButton.setText('Сбросить кол-во удачных ссылок')
        self.returnAcceptLinkButton.clicked.connect(self.retValLink)
        self.returnAcceptLinkButton.clicked.connect(self.data.save)


        self.saveButton = QtWidgets.QPushButton(self.frame)
        self.saveButton.move(420, 310)
        self.saveButton.resize(210, 30)
        self.saveButton.setText('Сохранить все настройки')
        self.saveButton.clicked.connect(self.data.save)



        self.isStartLastLink = QtWidgets.QCheckBox(self.frame)
        self.isStartLastLink.move(420, 365)
        self.isStartLastLink.setText('Пропустить пройденные аккаунты')
        self.isStartLastLink.setToolTip('Используйте только для старых ссылок\nДля новых ссылок снимите галочку')


        self.getFriendButton = Button(self.frame, 'Добавить', 'Добавляем...')
        self.getFriendButton.move(420, 390)
        self.getFriendButton.resize(100, 30)
        self.addThread = web.AddToFriends(self.getFriendButton, self.data)
        self.getFriendButton.clicked.connect(self.runAdd)

        self.delFriendButton = Button(self.frame, 'Удалить', 'Удаляем...')
        self.delFriendButton.move(530, 390)
        self.delFriendButton.resize(100, 30)
        self.delThread = web.DelFromFriends(self.delFriendButton, self.data)
        self.delFriendButton.clicked.connect(self.runDel)



        self.setFixedSize(640, 430)
        self.setWindowTitle('FriendsBot')
        self.setCentralWidget(self.frame)
        self.show()
        # self.setSt

    def retValLink(self):
        self.data.acceptLinkDay[1] = 0


    def runAdd(self):
        if not self.data.isRUN_ADD: 
            if self.switchMode:
                self.data.acceptLinkDay[1] = 0
                self.switchMode = False
            self.data.isRUN_ADD = True
            self.addThread.get_sheet()
            self.addThread.start()
            self.data.linkDay[0] = 0
        else:
            try:
                self.addThread.data.save()
                self.addThread.driver.close()
                self.delThread.f.close()
            except Exception as e: print(e)
            self.addThread.terminate()
            self.data.isRUN_ADD = False
            self.getFriendButton.setText('Добавить')

    def runDel(self):
        if not self.data.isRUN_DEL:
            if not self.switchMode:
                self.data.acceptLinkDay[1] = 0
                self.switchMode = True
            self.data.isRUN_DEL = True
            self.addThread.get_sheet()
            self.delThread.start()
            self.data.linkDay[0] = 0
        else:
            try:
                self.delThread.data.save()
                self.delThread.driver.close()
                self.delThread.f.close()
            except Exception as e: print(e)
            self.delThread.terminate()
            self.data.isRUN_DEL = False
            self.delFriendButton.setText('Удалить')


    def writeDay(self, number):
        day = self.data.days[number]
        self.isDayWorked.setChecked(day['power'])
        self.timeWorkLine.setText(day['time'])
        self.acceptLinkDayLine.setText(str(day['acceptLinkDay']))
        self.data.acceptLinkDay[0] = day['acceptLinkDay']
        print('Записал день')


class Button(QtWidgets.QPushButton):
    def __init__(self, parent=None, defaultText='Кнопка', workedText='Работаем'):
        super().__init__(parent=parent)

        self.defaultText = defaultText
        self.workedText  = workedText
        self.isWorked    = False

        self.setText(defaultText)
        self.clicked.connect(self.click)


    def click(self):
        if not self.isWorked:
            self.isWorked = True
            self.setText(self.workedText)
        else: 
            self.isWorked = False
            self.setText(self.defaultText)
        pass




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = Window()
    app.exec_()
    sys.exit()
    pass
