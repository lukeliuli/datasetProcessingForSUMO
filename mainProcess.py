import pandas as pd
import matplotlib.pyplot as plt
import time

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

for i,data in enumerate(veh_lane.unique()):
    if i==2:
        break
    #print(i,data)
    vehInOneLane = df[df.vehicle_lane==data]
    #print(vehInOneLane)
    lanePosX =  vehInOneLane.vehicle_x
    lanePosY =  vehInOneLane.vehicle_y
    maxTime = round(max(vehInOneLane.timestep_time))
    
    for t in range(maxTime):
        tmp  = vehInOneLane.vehicle_id.unique()
        print(t)
        #print(lanePosX)
        #plt.plot( lanePosX,lanePosY, '.')  # 蓝色圆点实线
        plt.ion()
        plt.figure(1)
        plt.plot( lanePosX,lanePosY, '.',color = 'black',linewidth=1,markersize=0.1,label='lane'),
        colorList= ['red','green','blue','yellow']
        for ii,data2  in enumerate(tmp):
            #print(t)
            veh = vehInOneLane[(vehInOneLane.vehicle_id == data2) & (vehInOneLane.timestep_time == float(t))] 
            #print(veh)
            if veh.empty:
                continue
            
            vehX =  veh.vehicle_x
            vehY =  veh.vehicle_y
            vehVel = veh.vehicle_speed
            vehTime  = veh.timestep_time
            
            
            plt.plot( vehX,vehY, 'o',color= colorList[ii%4],label=data2)  # 蓝色圆点实线 
            plt.legend()
            
        plt.show()
        plt.pause(0.001)
        plt.ioff()
        plt.clf()
        
      
        
    
    


#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()

