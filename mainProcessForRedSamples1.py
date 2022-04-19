import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib
from matplotlib.animation import FFMpegWriter
import string

import warnings 
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
print("#################################################################")

########################################################################################
#######枚举每一个车道,获得红灯附近的车，以及车道的长度
for i,curLaneID in enumerate(df.vehicle_lane.unique()):#枚举每一个车道

    #提取红灯时刻的车辆样本 LaneID:239331354_0 ; Time:4224.0 ; redID:VehicleFlowSouthToWest4.17
    if curLaneID != '239331354_0': #for debug
       continue


    redVehs =  pd.DataFrame(columns=df.columns)

    vehInOneLane = df[df.vehicle_lane==curLaneID]
    if vehInOneLane.empty == True:
        print("vehInOneLane.empty == True")
        continue
    maxLanePos =  max(vehInOneLane.vehicle_pos)#车道的长度



    vehInOneLane =vehInOneLane.sort_values(by='timestep_time',ascending=True)
    #########提取红灯车辆以及时刻
    timeList = vehInOneLane.timestep_time.unique()
    lowSpeedFlag = 0
    for t in timeList:#枚举每个时间
        title = "提取红灯车辆以及时刻,LaneID:"+str(curLaneID)+";"+"Time:"+str(t)+";"
        print(title)
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
               
          
   
    print("redVehs\n",redVehs.head())
    if redVehs.empty == True:
        print("redVehs.empty == True")
        input()
        continue
    
    ######对每条道路进行分析,当有车处于红灯状态时而且车道上有多个车时，给出红灯状态持续时间
    for i, redID in enumerate(redVehs.vehicle_id.unique()):
        
        #红灯状态的车辆ID
        redVehFocusTmp = redVehs[redVehs.vehicle_id == redID]#红灯状态的车辆ID
        timeList = redVehFocusTmp.timestep_time  # 红灯状态持续时间
        samples3 = []#收集当前车道内所有样本
        for t in timeList:#枚举红灯状态下的每个时间的每一辆车 
            
            title = "LaneID:"+str(curLaneID)+" ; "+"Time:"+str(t)+" ; "+"redID:"+redID
            print("提取红灯时刻的车辆样本",title)
            vehsAtTime = vehInOneLane[vehInOneLane.timestep_time == t] 
           
            if len(vehsAtTime.vehicle_id.unique()) == 1:  # 如果当前时间车辆只有一部车，统计忽略
                print("vehsAtTime.vehicle_id.unique()) == 1")
                continue


            vehsAtTime =vehsAtTime.sort_values(by='vehicle_pos',ascending=False)
            samples = []
            counter = 0
            
            for index, veh in vehsAtTime.iterrows():#每一辆车                  
                vehX =  veh.vehicle_x
                vehY =  veh.vehicle_y
                vehVel = veh.vehicle_speed
                vehTime  = veh.timestep_time
                vehID = veh.vehicle_id
                vehicle_Red_distane = maxLanePos - veh.vehicle_pos
                print("vehID,vehicle_Red_distane",vehID,vehicle_Red_distane)
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
                    samplesTmp.extend([0, 0]*(8-counter))#主车前面的车（最大8车）车辆的状态

                    samples2 = subject.copy()#主车
                    samples2.extend(samplesTmp)#主车前面的车（最大8车）+主车
                    samples3.append(samples2)#收集当前时间段内所有的样本
                    
                    #print("subject:",subject)
                    #print("samples:",samples)
                    #print("samplesTmp:",samplesTmp)
                    #print("samples2:",samples2)
                    
                        
                      
                samples.extend([vehicle_Red_distane, vehVel])
                counter = counter+1
               
            

            ##持续时间内的速度标志
            #提取红灯时刻的车辆样本 LaneID:239331354_0 ; Time:4223.0 ; redID:VehicleFlowSouthToWest4.17
            if t == 4224 and redID == 'VehicleFlowSouthToWest4.17': #for debug
               
               tmpArray = np.array(samples3)
               print(tmpArray.shape)
               print(tmpArray)
               


            tmpArray = np.array(samples3)
            minSpeed = min(tmpArray[:,3].astype(np.float))
            #print(tmpArray[:,3])
            #print(minSpeed,type(minSpeed))

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


            name1 = ["vehID","redLightTime","distToRedLight","speed","laneAvgSpeed","arriveTime1","arriveTime2"]   
            name2 = ["vehPos_1","vehSpeed_1","vehPos_2","vehSpeed_2","vehPos_3","vehSpeed_3","vehPos_4","vehSpeed_4"] 
            name3 = ["vehPos_5","vehSpeed_5","vehPos_6","vehSpeed_6","vehPos_7","vehSpeed_7","vehPos_8","vehSpeed_8"]
            headers = name1+name2+name3
            
            
            samplesTmp = pd.DataFrame(samples3,columns=headers)
            samplesTmp["speedFlag"]  = speedFlag #加一列，speedFlag
            filename = '.\\franceRedData\\'+curLaneID+'+'+redID+'.csv'
            samplesTmp.to_csv(filename)

            filename = '.\\franceRedData\\Platoon'+curLaneID+'+'+redID+'+Time@'+str(t)+'.csv'
            #print(filename)
            #print("vehsAtTime.head()\n",vehsAtTime.head())
            vehsAtTime.to_csv(filename)
           

            
            
            
          
   

    #writer.finish()
    
    
    




#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()

