import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib
from matplotlib.animation import FFMpegWriter
import string

import warnings 
from tqdm import tqdm
warnings.filterwarnings('ignore')
###################################################################################################
#############主程序

df = pd.read_csv('.\data\data1.csv',sep = ';')
print("#################################################################")
print("df.head()\n",df.head())
#print("df.info()\n",df.info())
#print(df.describe())


print("#################################################################")
print("veh_lane.unique()\n",df.vehicle_lane.unique())
laneList = df.vehicle_lane.unique()
numLanes = len(df.vehicle_lane.unique())
print("numLanes \n",numLanes)
print("#################################################################")


########################################################################################
#######枚举每一个车道,获得红灯附近的车，以及车道的长度
#for ilane,curLaneID in enumerate(df.vehicle_lane.unique()):#枚举每一个车道
for ilane in tqdm(range(numLanes)):#枚举每一个车道
    curLaneID= laneList[ilane]
    print(ilane,numLanes,curLaneID)
    #提取红灯时刻的车辆样本 LaneID:239331354_0 ; Time:4224.0 ; redID:VehicleFlowSouthToWest4.17
    #if curLaneID != '239331354_0': #for debug
    #   continue

    #1.获得车道长度
    redVehs =  pd.DataFrame(columns=df.columns)

    vehInOneLane = df[df.vehicle_lane==curLaneID]
    if vehInOneLane.empty == True:
        print("vehInOneLane.empty == True")
        continue
    maxLanePos =  max(vehInOneLane.vehicle_pos)#车道的长度

    ############################################################3
    #2.提取红灯车辆以及时刻
    vehInOneLane =vehInOneLane.sort_values(by='timestep_time',ascending=True)
   
    timeList = vehInOneLane.timestep_time.unique()
    lowSpeedFlag = 0
    for t in timeList:#枚举每个时间
        title = "2.提取红灯车辆以及时刻,LaneID:"+str(curLaneID)+";"+"Time:"+str(t)+";"
        #print(title)
        vehsAtTime = vehInOneLane[vehInOneLane.timestep_time == float(t)] 

        for index, veh in vehsAtTime.iterrows():#每一辆车
            #print(index,veh)
            vehX =  veh.vehicle_x
            vehY =  veh.vehicle_y
            vehVel = veh.vehicle_speed
            vehTime  = veh.timestep_time
            vehID = veh.vehicle_id
            vehicle_pos = veh.vehicle_pos
            if (vehVel <1) and (abs(vehicle_pos - maxLanePos)<1):
                lowSpeedFlag = 1
                redVehs.loc[len(redVehs.index)] =veh
               
          
   
    #print("redVehs\n",redVehs.head())
    if redVehs.empty == True:
        print("redVehs.empty == True")
        #input()
        continue
    
    #3.当有车处于红灯状态时而且车道上有多个车时,对每条道路进行分析
    speedFlagDict = {}
    for ired, redID in enumerate(redVehs.vehicle_id.unique()):
        
       
        redVehFocusTmp = redVehs[redVehs.vehicle_id == redID]#红灯状态的车辆ID
        timeList = redVehFocusTmp.timestep_time.values  # 红灯状态持续时间
        
        
        #3.1 枚举当前道路上红灯状态下的时间内所有车，并获得最小速度
        locTmp1 = vehInOneLane.timestep_time >= min(timeList)
        locTmp2 = vehInOneLane.timestep_time <= max(timeList)
        locTmp3 = abs(maxLanePos - vehInOneLane.vehicle_pos)<100 #距离红灯100米以内
        
        vehsAtTimeAndDist = vehInOneLane[locTmp1 & locTmp2]
        vehIDsAtTimeAndDist = vehsAtTimeAndDist.vehicle_id.unique()
        #print("3.1 枚举当前道路上红灯状态下的时间内所有车，并获得最小速度",vehIDsAtTimeAndDist)
        for ii,idTmp  in enumerate(vehIDsAtTimeAndDist):
            vehTmp = vehsAtTimeAndDist[vehsAtTimeAndDist.vehicle_id==  idTmp]
            minSpeed = min(vehTmp.vehicle_speed.values)
            if minSpeed >= 40/3.6:
                speedFlag  = 4
            if minSpeed <40/3.6 and minSpeed> 30/3.6:
                speedFlag  = 3
            if minSpeed <30/3.6 and minSpeed> 20/3.6:
                speedFlag  = 2
            if minSpeed <20/3.6 and minSpeed> 10/3.6:
                speedFlag  = 1
            if minSpeed <10/3.6:
                speedFlag  = 0
 
            speedFlagDict[idTmp] = speedFlag

        #3.2 枚举当前道路上红灯状态下的每个时间的每一辆车，并生成样
        samples3 = []#收集当前车道内对应红车有样本
        for t in timeList:#枚举红灯状态下的每个时间的每一辆车 
            
            title = "LaneID:"+str(curLaneID)+" ; "+"Time:"+str(t)+" ; "+"redID:"+redID
            #print("3.2 提取红灯时刻的车辆样本",title)
            locTmp1 =  vehInOneLane.timestep_time == t      
            locTmp2 = abs(maxLanePos - vehInOneLane.vehicle_pos)<100 #距离红灯100米以内

            vehsAtTime = vehInOneLane[locTmp1 & locTmp2] 
            
            if len(vehsAtTime.vehicle_id.unique()) == 1:  # 如果当前时间车辆只有一部车，统计忽略
                #print("vehsAtTime.vehicle_id.unique()) == 1")
                continue


            vehsAtTime =vehsAtTime.sort_values(by='vehicle_pos',ascending=False)
            samples = []
            counter = 0
            
            #3.2.1 枚举当前道路上红灯状态下的每个时间的每一辆车，并生成每个时刻样本
            for rowindex, veh in vehsAtTime.iterrows():#每一辆车                  
                vehX =  veh.vehicle_x
                vehY =  veh.vehicle_y
                vehVel = veh.vehicle_speed
                vehTime  = veh.timestep_time
                vehID = veh.vehicle_id
                vehicle_Red_distane = maxLanePos - veh.vehicle_pos
                #print("vehID:",vehID," vehicle_Red_distane:",vehicle_Red_distane)
                samples2 = []
                if counter == 0 and vehID != redID:
                    print("counter == 0,redID:",redID,"vehID",vehID)
                    input()
                    break

                    

                if counter > 0:
                    avg_speed_lane = 60/3.6
                    max_speed_lane = 80/3.6
                    subject = [vehID,max(timeList) - t,#主车状态
                    vehicle_Red_distane,
                    vehVel,
                    avg_speed_lane,
                    vehicle_Red_distane/(vehVel+0.01),
                    vehicle_Red_distane/avg_speed_lane]
                    
                    samplesTmp = samples.copy()
                    samplesTmp.extend([0, 0]*(20-counter))#主车前面的车（最大20车）车辆的状态

                    samples2 = subject.copy()#当前样本：主车
                    samples2.extend(samplesTmp)#当前样本：主车+主车前面的车（最大20车）
                    samples2.extend([speedFlagDict[vehID]])#当前样本：主车+主车前面的车（最大20车）+speedFlag
                    samples3.append(samples2)#收集当前时间段内所有的样本
                    
                    #print("subject:",subject)
                    #print("samples:",samples)
                    #print("samplesTmp:",samplesTmp)
                    #print("samples2:",samples2)
                    
                        
                      
                samples.extend([vehicle_Red_distane, vehVel])
                counter = counter+1
               
            

               
       



            #记录当前时刻排队情况
            #filename = '.\\franceRedData\\Platoon'+str(ilane)+redID+'+Time@'+str(t)+'.csv'
            #print(filename)
            #print("vehsAtTime.head()\n",vehsAtTime.head())
            #vehsAtTime.to_csv(filename)
        
        
        #当前车道，每个红灯车的所有时刻的样本
        name1 = ["vehID","redLightTime","distToRedLight","speed","laneAvgSpeed","arriveTime1","arriveTime2"]   
        name2 = ["vehPos_1","vehSpeed_1","vehPos_2","vehSpeed_2","vehPos_3","vehSpeed_3","vehPos_4","vehSpeed_4"] 
        name3 = ["vehPos_5","vehSpeed_5","vehPos_6","vehSpeed_6","vehPos_7","vehSpeed_7","vehPos_8","vehSpeed_8"]
        name4 = ["vehPos_9","vehSpeed_9","vehPos_10","vehSpeed_10","vehPos_11","vehSpeed_11","vehPos_12","vehSpeed_12"]
        name5 = ["vehPos_13","vehSpeed_13","vehPos_14","vehSpeed_14","vehPos_15","vehSpeed_15","vehPos_16","vehSpeed_16"]
        name6 = ["vehPos_17","vehSpeed_17","vehPos_18","vehSpeed_18","vehPos_19","vehSpeed_19","vehPos_20","vehSpeed_20"]
        headers = name1+name2+name3+name4+name5+name6+["speedFlag"]

        if samples3 != []:
            samplesTmp = pd.DataFrame(samples3,columns=headers)
            filename = '.\\franceRedData\\'+str(ilane)+'+'+redID+'.csv'
            samplesTmp.to_csv(filename,float_format='%.3f',index=0) 


###################################################################################
#将所有样本集合成一个CSV文件
import os
import pandas as pd
path = ".\\franceRedData\\"

filelist = [path + i for i in os.listdir(path)]
dataset = pd.read_csv(filelist[0])

for tmpFile in filelist:
    if tmpFile.endswith(".csv"):
        #print(tmpFile)
        tmpDF = pd.read_csv(tmpFile)
        dataset = pd.concat([dataset,tmpDF],ignore_index=True,axis=0)
        

filename= path+"0_allSamples.csv" 
dataset.to_csv(filename,float_format='%.3f',index=0) 
        

