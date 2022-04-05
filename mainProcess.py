import pandas as pd
import matplotlib.pyplot as plt
import time

from matplotlib.animation import FFMpegWriter


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
fg1 = plt.figure()

metadata = dict(title='france Dataset traces', artist='lukeliuli',comment='france Dataset traces')
writer = FFMpegWriter(fps=15, metadata=metadata)

with writer.saving(fg1, "franceDataset.mp4", 600):

    df = mulVehsOneLane
    for i,data in enumerate(df.vehicle_lane.unique()):
        if i==2:
            break
        vehInOneLane = df[df.vehicle_lane==data]
        #print(vehInOneLane)
        lanePosX =  vehInOneLane.vehicle_x
        lanePosY =  vehInOneLane.vehicle_y
        maxTime = round(max(vehInOneLane.timestep_time))
        minTime = round(min(vehInOneLane.timestep_time))
        
        for t in range(minTime,maxTime):
            tmp  = vehInOneLane.vehicle_id.unique()
            print(t)
            #print(lanePosX)
            #plt.plot( lanePosX,lanePosY, '.')  # 蓝色圆点实线
            #plt.ion()
            
            plt.plot( lanePosX,lanePosY, '.',color = 'black',linewidth=1,markersize=0.1,label='lane'),
            colorList= ['red','green','blue','yellow']
            title = "time:"+str(t)+";"
            for ii,data2  in enumerate(tmp):
                #print(t)
                veh = vehInOneLane[(vehInOneLane.vehicle_id == data2) & (vehInOneLane.timestep_time == float(t))] 
                #print(veh)
                if veh.empty:
                    continue
                
                vehX =  veh.vehicle_x
                vehY =  veh.vehicle_y
                vehVel = veh.vehicle_speed.to_numpy()
                vehTime  = veh.timestep_time
                
                title = title+"\n"+data2+",Speed:"+str(vehVel)+";"
                plt.plot( vehX,vehY, 'o',color= colorList[ii%4],label=data2)  # 蓝色圆点实线 
                plt.legend()
            
            plt.title(title)    
            #plt.show()
            writer.grab_frame()
            plt.pause(1)
            #plt.ioff()
            plt.clf()
        
      
        
    
    


#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()

