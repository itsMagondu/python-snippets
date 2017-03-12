__author__ =  "SamuelMagondu"
__version__ = "python2.7"

import dateutil.parser
import datetime
import urllib2
import urllib
import json

def get_current_time():
	#Get time and date in ISO 8601 format
	return datetime.datetime.now().isoformat()	

def convert_to_unix_time(mytime):
	#Convert to unix time format. Ensure the timezone info is accounted for
	parsed_t = dateutil.parser.parse(mytime)
	return parsed_t.strftime('%s')

def sum_unix_time(unix_time):
	#Add all numbers in unix_time
	sum_time = 0
	for item in unix_time:
		try:
			sum_time += int(item)
		except ValueError:
			print ("Value error, cannot parse to int")
			raise
		except Exception as e:
			print (e)
			raise
	return sum_time

def pull_apixu_data():
	#Get data from API
	apixu_api = 'http://api.apixu.com/v1/current.json?key=a4dc37f03e95452a8b771527171103&q=Nairobi'
	response = urllib2.urlopen(apixu_api)
	apixu_data = json.loads(response.read())
	print ("\n...... Nairobi weather data .....")
	print (apixu_data)
	return apixu_data

def post_collected_data(apixu_data, unix_time, sum_time, mytime):
	#Create post data
	to_post = {}
	to_post['name'] = "Samuel Magondu"
	to_post['humidity'] = apixu_data['current']['humidity']
	to_post['unix'] = unix_time
	to_post['sum'] = sum_time
	to_post['timestamp'] =mytime
	to_post['temperature_celsius'] = apixu_data['current']['temp_c']

	#Do post
	post_url = 'https://hooks.zapier.com/hooks/catch/1604383/mw5sh8/'
	data = urllib.urlencode(to_post)
	request = urllib2.Request(post_url, data)
	response = urllib2.urlopen(request)
	status = response.read()
	return status

if __name__ == "__main__":
	mytime = get_current_time()
	unix_time = convert_to_unix_time(mytime)
	sum_time = sum_unix_time(unix_time)
	apixu_data = pull_apixu_data()
	status = post_collected_data(apixu_data, unix_time, sum_time, mytime)
	print ("\n...... post status .....")
	print (status)
