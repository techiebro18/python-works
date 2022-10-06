import matplotlib.pyplot as plt
import csv

x = []
y = []
with open("customers_bought_channels.csv", "r") as csvfile:
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

plt.plot(x, y, color = 'g', linestyle = 'dashed', marker = 'o', label = "Orders")
plt.subplots_adjust(bottom=0.25)
plt.xticks(rotation = 25)
plt.xlabel('Channels')
plt.ylabel('Orders')
plt.title('Orders from Channels')
plt.legend()
plt.show()
