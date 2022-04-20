import csv
import numpy as np
file1 = "./franceRedData/0_allSamples.csv"
csvfile = open(file1, 'r')
xyData= np.loadtxt(file1,delimiter=',',skiprows=1,usecols=list(range(1,48)))
x = xyData[:,0:-1]
y = xyData[:,-1]

print(y.shape )
print(x.shape )