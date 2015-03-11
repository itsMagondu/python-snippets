import csv


f = "/home/magondu/numberformat.csv"
print f

numbers = []
with open(f,'rb') as csvfile:
    fOpen = csv.reader(csvfile)
    print fOpen

    for row in fOpen:
        x = row[0]
        if x[:1] == "7":
            x = "+254" + x
        else:
            pass

        if len(x) < 13:
            x = "Invalid number : " + str(x)
        numbers.append(x)
        print x

print numbers
with open('/home/magondu/finalfile.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for item in numbers:
        writer.writerow(str(item))

