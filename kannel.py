import requests

c = 0
while c < 100:
    x = requests.get("http://127.0.0.1:13013/cgi-bin/sendsms?username=kannel&password=kannel&to=+254700040007&text=engine")
    print x
    c+=1
