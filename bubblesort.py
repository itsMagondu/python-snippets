x = [12,1,2,5,7,3,5,1,3,10,1,8,2,3,1]

for i in range(len(x)-1,0,-1):
    print i
    for j in range(i):
        if x[j]>x[j+1]:
            temp = x[j]
            x[j] = x[j+1]
            x[j+1] = temp
    print x

print x
