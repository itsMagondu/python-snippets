# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys

tot = sys.stdin.readline().strip()

try:
    tot = int(tot)
except ValueError:
    pass

    
def fibTest(f0,f1,f,num):
    f0 = f1   
    f1 = f
    f = f0+f1
    
    if int(f) < int(num):
          f0,f1,f,num = fibTest(f0,f1,f,num)
    else:
        if f == int(num):
            print "IsFibo"
        else:
            print "IsNotFibo"
    return f0,f1,f,num
def getFibnumber(f0,f1):
    return f0+f1

while tot:
    num = sys.stdin.readline().strip()
    f0 = 0
    f1 = 1
    f = getFibnumber(f0,f1)

    try:
        num = int(num)
        if num != 0 or num != 1:
            fibTest(f0,f1,f,num)

        tot -= 1

    except ValueError:
        pass

    
