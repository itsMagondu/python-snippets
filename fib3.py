loops = 4000
n1,n2,n3 = [1,1,1]
n = 0
while loops > 3:
    n = n1+n2+n3
    n1 =n2
    n2 = n3
    n3 = n
    loops -= 1
print n
