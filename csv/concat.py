import csv

csv_file = open('file.csv', newline='')
reader = csv.reader(csv_file, delimiter=',')
data = list(reader)
newstr = ''
for item in data:
    print(item[0])
    newstr = newstr+','+item[0]


print(newstr)
