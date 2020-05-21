import matplotlib.pyplot as plt
import csv
import numpy as np

x=[]
y=[]
fig = plt.figure()
ax = fig.add_subplot(111)
with open('ds.csv', 'r') as file:
    plots= csv.reader(file, delimiter=',')
    for row in plots:
        x.append(float(row[2]))
        y.append(float(row[3]))

ax.plot(x,y)
ax.set_yticks(np.arange(min(y), max(y)+1, 1.0)) # setting the ticks
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.show()
# plt.plot(x,y, marker='o')

# plt.title('Data from the CSV File: People and Expenses')



# plt.show()



