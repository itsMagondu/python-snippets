import sys

tot = sys.stdin.readline().strip()
try:
    tot = int(tot)
except ValueError:
    pass

while tot:
    digits = 0
    num = sys.stdin.readline().strip()
    if num != 0:
        for item in str(num).strip():
            if int(item) != 0:
                if int(num)%int(item) == 0:
                    digits +=1
    tot -= 1
    print tot
