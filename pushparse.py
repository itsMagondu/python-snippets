from xml.etree import ElementTree as ET

#str = '<sms-response delivery-notification-requested="true" version="1.0"><message id="1"ref-id="54321"msisdn="+79991234567"service-number="1234"operator="operator-smpp"defer-date="2008-10-15 10:00:00"validity-period="3"priority="1"><content type="text/plain">Response on message</content></message></sms-response>'
st = '<sms-response login="test" password="pass" delivery-notification-requested="true" version="1.0"><message id="1" ref-id="54321" msisdn="+79991234567" service-number="1234" operator="operator-smpp" defer-date="2008-10-15 10:00:00" validity-period="3" priority="1"><content type="text/plain">Response on message</content></message></sms-response>'
#xml = request.raw_post_data
m = ET.XML(st)

x = None
for i in m:    
    print i.attrib
    print dir(i)
    x = i.getchildren()
    print x[0].text
    print i.attrib.get('id')
    print i.attrib.get('service-number')
    print i.attrib.get('msisdn')
    print i.attrib.get('ref-id')
    print i.attrib.get('operator')
    print i.attrib.get('defer-date')
    

