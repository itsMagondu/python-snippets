doub = True

h = 1
cyc = 10

while cyc:
    if doub == True:
        h = h*2
        doub = False
    else:
        h = h+1
        doub = True
    print h
    cyc = cyc -1
