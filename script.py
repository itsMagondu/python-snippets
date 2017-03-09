# __Author__: SamuelMagondu 

import dateutil.parser
import datetime


#Get time and date in ISO 8601 format
mytime = datetime.datetime.now().isoformat()

#Conver to unix time format. Ensure the timezone info is accounted for
parsed_t = dateutil.parser.parse(mytime)
mytime_in_seconds = parsed_t.strftime('%s')

#Add all numbers in mytime_in_seconds
total = 0
for item in mytime_in_seconds:
	total += item

#Get data from API