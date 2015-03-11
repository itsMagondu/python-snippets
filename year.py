this_year = 2013
year = 1970

print this_year,year
print (this_year - 10)
group1=0
group2=0
group3=0
group4=0


if (2003>= 1970 and 1963 <=1970):
    print "yes"
if (year <= (this_year - 10) and year >= (this_year - 30)):
    group1 += 1
elif (year < (this_year - 30)  and year >= (this_year - 50)):
    group2 += 1
elif (year < (this_year - 50)  and year >= (this_year - 70)):
    group3 += 1
elif (year < (this_year - 70)  and year >= (this_year - 90)):
    group4 += 1
else:
    print this_year-year
    print "Unknown date"

print group1,group2,group3,group4
