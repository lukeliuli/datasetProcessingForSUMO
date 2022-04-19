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
#matplotlib.use("Agg")
print(FFMpegWriter.bin_path())

df = pd.read_csv('.\data\data1.csv',sep = ';')
print("#################################################################")
print("df.head()\n",df.head())
#print("df.info()\n",df.info())
#print(df.describe())
#veh_lane1 = df[df.vehicle_lane=='-1356_0']
print("#################################################################")
print("veh_lane1\n",veh_lane1)

veh_lane = df.vehicle_lane
print("#################################################################")
print("veh_lane.unique()\n",veh_lane.unique())
print("#################################################################")

print("#################################################################")
print("显示多车同一车道")
print("#################################################################")


df1=df.groupby(["vehicle_lane","timestep_time"]).size()
#print(df1)
col=df1[df1>1].reset_index()[["vehicle_lane","timestep_time"]]
#print(col)
mulVehsOneLane = pd.merge(col,df,on=["vehicle_lane","timestep_time"])
print(mulVehsOneLane)
#input()

print("#################################################################")
print("显示轨迹")
print("#################################################################")


fg1= plt.figure(figsize=(8,5))
metadata = dict(title='france Dataset traces', artist='lukeliuli',comment='france Dataset traces')
writer = FFMpegWriter(fps=5, metadata=metadata)


#df = mulVehsOneLane
for i,curLaneID in enumerate(df.vehicle_lane.unique()):#枚举每一个车道
    
    vehInOneLane = df[df.vehicle_lane==curLaneID]
    if vehInOneLane.empty == True:
        continue
    maxLanePos =  max(vehInOneLane.vehicle_pos)
    vehInOneLane =vehInOneLane.sort_values(by='timestep_time',ascending=True)

    redFlagRecord = vehInOneLane.drop(index=vehInOneLane.index)

    #画车道图
    lanePosX =  vehInOneLane.vehicle_x.to_numpy()
    lanePosY =  vehInOneLane.vehicle_y.to_numpy()
    lanePosXT = lanePosX[:len(lanePosX):10]
    lanePosYT = lanePosY[:len(lanePosY):10]
    #plt.plot( lanePosXT,lanePosYT, '.',color = 'black',linewidth=1,markersize=0.1,label='lane')
    
    #writer.setup(fg1, str(i)+"-"+"laneID("+str(curLaneID)+").mp4", dpi=600)
    #提取时刻
    timeList = vehInOneLane.timestep_time.unique()
    lowSpeedFlag = 0
    for t in timeList:#枚举每个时间
        title = "LaneID:"+str(curLaneID)+";"+"Time:"+str(t)+";"
        print(title)
        

        colorList= ['r', 'g', 'b', 'y', 'c', 'm', 'k']
        
        vehsAtTime = vehInOneLane[vehInOneLane.timestep_time == float(t)] 
 
        for index, veh in vehsAtTime.iterrows():#每一辆车
            #print(index,veh)
            vehX =  veh.vehicle_x
            vehY =  veh.vehicle_y
            vehVel = veh.vehicle_speed
            vehTime  = veh.timestep_time
            vehID = veh.vehicle_id
            vehicle_pos = veh.vehicle_pos
            #title = title+"\n"+vehID+",Speed:"+str(vehVel)+";"
     
            randNum =sum([ord(x) for x in str(vehID)])
            #plt.plot( vehX,vehY, 'o',color= colorList[randNum%7],label=vehID)  # 蓝色圆点实线 
            #plt.annotate(str(vehVel)+","+str(vehicle_pos)+','+vehID, xy=(vehX,vehY),  xytext=(-50, 10), textcoords='offset points')
            #plt.plot( lanePosXT,lanePosYT, '.',color = 'black',markersize=0.1,label='lane')
            if vehVel <1 & (abs(vehicle_pos - maxLanePos)<1):
                lowSpeedFlag = 1
                #plt.annotate("redLight", xy=(vehX,vehY),  xytext=(-50, 20), textcoords='offset points')
                #print("redLight"+vehID)
                redFlagRecord = redFlagRecord.append(veh, ignore_index=True)
          
               

        
            
        #plt.legend()
        #plt.title(title,fontsize='xx-small')    
        #plt.show()
        #writer.grab_frame()
        #plt.ioff()
        #plt.cla()
    
    ######对每条道路进行分析,当有车处于红灯状态时而且车道上有多个车时，给出红灯状态持续时间
    redVehs = redFlagRecord.vehicle_id.unique()#红灯状态的车辆ID
    for i, redID in enumerate(redVehs):
        
        #红灯状态的车辆ID
        redFlagRecordTMP = redFlagRecord[redFlagRecord.vehicle_id == redID]#红灯状态的车辆ID
        timeList = redFlagRecordTMP.timestep_time  # 红灯状态持续时间
        indexTmp = (vehInOneLane.timestep_time >= min(timeList)) & (vehInOneLane.timestep_time <= max(timeList))
        vehsAtRedTime = vehInOneLane[indexTmp]  # 获得红灯状态持续时间内，车道内的车辆数目
       
        if len(vehsAtRedTime.vehicle_id.unique()) > 1:

            samples3 = []
            for t in timeList:#枚举红灯状态下的每个时间
                #print("currentTime:",t)
                vehsAtTime = vehInOneLane[vehInOneLane.timestep_time == t] 
                #print("vehicle_id.unique()\n", vehsAtTime.vehicle_id.unique())
               
                if len(vehsAtTime.vehicle_id.unique()) == 1:  # 如果当前时间车辆只有一部车，统计忽略
                    continue


                vehsAtTime =vehsAtTime.sort_values(by='vehicle_pos',ascending=False)
                
                #print([vehsAtTime.timestep_time.to_numpy(),vehsAtTime.vehicle_id.to_numpy(),vehsAtTime.vehicle_pos.to_numpy()])
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
                        samples2.extend(samplesTmp)#主车前面的车（最大8车）
                        samples3.append(samples2)#收集当前时间段内所有的样本
                        
                        #print("subject:",subject)
                        #print("samples:",samples)
                        #print("samplesTmp:",samplesTmp)
                        print("samples2:",samples2)
                        
                        
                      
                    samples.extend([vehicle_Red_distane, vehVel])
                    counter = counter+1
            

            ##持续时间内的速度标志
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
            
            
          
   

    #writer.finish()
    
    
    




#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()

