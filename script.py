# __Author__: SamuelMagondu 

import dateutil.parser
import datetime
import urllib2
import urllib
import json


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
response = urllib2.urlopen('http://api.apixu.com/v1/current.json?key=a4dc37f03e95452a8b771527171103&q=Nairobi')
weather_data = json.loads(response)

#Create post data
to_post = {}
to_post['name'] = "Samuel Magondu"
to_post['humidity'] = weather_data['current']['humidity']
to_post['unix'] = mytime_in_seconds
to_post['sum'] = total
to_post['timestamp'] =mytime
to_post['temperature_celsius'] = weather_data['current']['temp_c']

#Do post
post_url = 'https://hooks.zapier.com/hooks/catch/1604383/mw5sh8/'
data = urllib.urlencode(to_post)
request = urllib2.Request(post_url, data)
response = urllib2.urlopen(request)
status = response.read()

#Unit tests
#Add function you can call