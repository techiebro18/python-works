import matplotlib.pyplot as plt
import csv

x = []
y = []
with open("brands_orders.csv", "r") as csvfile:
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0) 
    plots = csv.reader(csvfile, delimiter = ',')
    #print(plots)
    if has_header:
        next(plots)  # Skip header row.

    for row in plots:
        #print(row)
        x.append(row[0])
        y.append(int(row[1]))

plt.subplots_adjust(bottom=0.30)
plt.xticks(rotation = 70)
plt.bar(x, y, color = 'g', width = 0.72, label = "Age")
plt.xlabel('Brands')
plt.ylabel('Count')
plt.title('Brands with Count')
plt.legend()
plt.show()
