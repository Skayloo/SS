import json
import datetime
import time

print(datetime.datetime.now().hour)
quit()

days = {
    '1':{
      "power":  True,
      "time":   "10.10-20.00",
      "pauses": ["12.10-13.10", "21.00-33.00"]
    },

    '2':{
      "power":  True,
      "time":   "10.00-20.00",
      "pauses": ["12.10-13.10", "21.00-33.00"]
    }
}

# data = json.loads(text)

day = days['1']





def check(day={}):
	power   = bool(day['power'])
	if not power: return False

	work_t  = day['time'].split('-')
	pauses  = day['pauses']
	ts = float(work_t[0])
	tf = float(work_t[1])
	tn = 20.20
	if ts < tn < tf:
		for pause_t in pauses:
			pause_t = pause_t.split('-')
			ts = float(pause_t[0])
			tf = float(pause_t[1])
			
			if ts < tn < tf: 
				return False
		return True
	return False

for k in days:
	print(check(days[k]))
# print(f"{power}\n{work_t}\n{pauses}")

