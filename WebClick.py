import datetime
import os
import time
import random

import pyautogui



def click(x, y):
    pass



def check(day):
	power   = day['power']
	if not power: return False

	work_t  = day['time'].split('-')
	pauses  = day['pauses']
	ts = float(work_t[0])
	tf = float(work_t[1])
	tn = float(f'{datetime.datetime.now().hour}.{datetime.datetime.now().minute}')
	if ts < tn < tf:
		for pause_t in pauses:
			pause_t = pause_t.split('-')
			ts = float(pause_t[0])
			tf = float(pause_t[1])
			
			if ts < tn < tf: 
				return False
		return True
	return False



def runWeb_addFriends(data, getFriendButton):
    if data.isStartLastLink: k = data.acceptLinks - 1
    else: k = 0

    result = 0
    while k < len(data.links):
        print(k)
        time.sleep(random.randint(int(data.delay[0]), int(data.delay[1])))

        if check(data.days[str(datetime.datetime.now().weekday() + 1)]):
            try: 
                link = data.links[k].replace(',', '') if data.links[k].replace(',', '') != None else data.links[k]
                link = link.replace("'", '') if link.replace("'", '') != None else link
                link = link.replace("'", '') if link.replace("'", '') != None else link
            except IndexError: return
            
            result = addFriend(data, getFriendButton, link)

        if result == 3: break
        if result == 2: time.sleep(10)
        data.save()
        
        k += result
        data.acceptLinks += 1

    data.save()
    getFriendButton.setText('Добавление в друзья')



def addFriend(data, getFriendButton, link):
    if data.acceptLinks >= data.maxLinks: return 3

    rating = 0

    if rating <= data.rating:
            for k in []:
                if (((k.text == 'jobs' or k.text == 'работы')       and data.isCheckJobs) or 
                    ((k.text == 'products' or k.text == 'продукты') and data.isCheckProducts) or
                    ((k.text == 'signals' or k.text == 'сигналы')   and data.isCheckSignals)): return 1
    return 1




if __name__ == "__main__":
    
    pass