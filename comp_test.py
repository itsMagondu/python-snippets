import requests as r

payload = {'rec': '+254723453841', 'amount': '5','key':'54321','domain':'safaricom',}

x = r.post('http://75.101.179.171/comp/compensate/put/',data = payload)
#x = r.post('http://192.168.1.28/comp/compensate/put/',data = payload)

print x.text

t = open("Output.html", "w")

t.write(x.text)

t.close
