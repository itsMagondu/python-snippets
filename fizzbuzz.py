c = 101

for i in xrange(1,c):
    string = ''
    if i %3 == 0:
        string += "fizz"
    if i % 5 == 0:
        string += "buzz"
    if not string:
        string = i
    print string
