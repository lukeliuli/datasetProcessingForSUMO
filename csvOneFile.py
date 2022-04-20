#将所有样本集合成一个CSV文件
import os
import pandas as pd
path = ".\\franceRedData\\"

filelist = [path + i for i in os.listdir(path)]
dataset = pd.read_csv(filelist[0])
print(dataset.tail())
input()
for tmpFile in filelist:
    if tmpFile.endswith(".csv"):
        #print(tmpFile)
        tmpDF = pd.read_csv(tmpFile)
        dataset = pd.concat([dataset,tmpDF],ignore_index=True,axis=0)
        

filename= path+"0_AllData.csv" 
dataset.to_csv(filename,float_format='%.3f',index=0) 
        
    