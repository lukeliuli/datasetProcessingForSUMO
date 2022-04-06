import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib
from matplotlib.animation import FFMpegWriter

matplotlib.use("Agg")
print(FFMpegWriter.bin_path())

df = pd.read_csv('.\data\data1.csv',sep = ';')
print("#################################################################")
print("df.head()\n",df.head())
#print("df.info()\n",df.info())
#print(df.describe())
veh_lane1 = df[df.vehicle_lane=='-1356_0']
print("#################################################################")
print("veh_lane1\n",veh_lane1)

veh_lane = df.vehicle_lane
print("#################################################################")
#print("veh_lane.unique()\n",veh_lane.unique())
print("#################################################################")

print("#################################################################")
print("显示多车同一车道")
print("#################################################################")


df1=df.groupby(["vehicle_lane","timestep_time"]).size()
#print(df1)
col=df1[df1>1].reset_index()[["vehicle_lane","timestep_time"]]
#print(col)
mulVehsOneLane = pd.merge(col,df,on=["vehicle_lane","timestep_time"])
#print(mulVehsOneLane)
#input()

print("#################################################################")
print("显示轨迹")
print("#################################################################")


fg1= plt.figure(figsize=(8,5))
metadata = dict(title='france Dataset traces', artist='lukeliuli',comment='france Dataset traces')
writer = FFMpegWriter(fps=1, metadata=metadata)


df = mulVehsOneLane
for i,curLaneID in enumerate(df.vehicle_lane.unique()):#枚举每一个车道

    
    writer.setup(fg1, "curLaneID-"+str(i)+".mp4", dpi=600)

    vehInOneLane = df[df.vehicle_lane==curLaneID]
    maxTime = round(max(vehInOneLane.timestep_time))
    minTime = round(min(vehInOneLane.timestep_time))
    
    for t in range(minTime,maxTime):#枚举每个时间
        print("laneID:%s,time:%d" %(curLaneID ,t))
        vehsAtTime = vehInOneLane[vehInOneLane.timestep_time == float(t)] 
        if vehsAtTime.empty:
                continue
        
      
        #画车道图git
        lanePosX =  vehInOneLane.vehicle_x
        lanePosY =  vehInOneLane.vehicle_y
        plt.plot( lanePosX,lanePosY, '.',color = 'black',linewidth=1,markersize=0.1,label='lane'),
        colorList= ['red','green','blue','yellow']
        title = "time:"+str(t)+";"

    
        for index, veh in vehsAtTime.iterrows():#每一辆车
            #print(index,veh)
            vehX =  veh.vehicle_x
            vehY =  veh.vehicle_y
            vehVel = veh.vehicle_speed
            vehTime  = veh.timestep_time
            vehID = veh.vehicle_id
            
            #title = title+"\n"+vehID+",Speed:"+str(vehVel)+";"
            plt.plot( vehX,vehY, 'o',color= colorList[int(vehID[-1])%4],label=vehID)  # 蓝色圆点实线 
            plt.annotate(str(vehVel)+","+vehID,xy=(vehX, vehY),  xytext=(-50, 10), textcoords='offset points')
            
        #plt.legend()
        plt.title(title,fontsize='xx-small')    
        #plt.show()
        writer.grab_frame()
        #plt.ioff()
        plt.cla()

    writer.finish()
    
    
    




#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()

