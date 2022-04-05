import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data1.csv',sep = ';')
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
    #print(i,data)
    vehInOneLane = df[df.vehicle_lane==data]
    #print(vehInOneLane)
    lanePosX =  vehInOneLane.vehicle_x
    lanePosY =  vehInOneLane.vehicle_y
    maxTime = round(max(vehInOneLane.timestep_time))
    
    for t in range(maxTime):git 
        tmp  = vehInOneLane.vehicle_id.unique()
        print(len(tmp))
        #print(lanePosX)
        #plt.plot( lanePosX,lanePosY, '.')  # 蓝色圆点实线
        
        for data2  in tmp:
            print(data2)
            veh = vehInOneLane[vehInOneLane.vehicle_id==tmp & vehInOneLane.timestep_time == t]
            if veh == None:
                continue
            
            vehX =  veh.vehicle_x
            vehY =  veh.vehicle_y
            vehVel = veh.vehicle_speed
            vehTime  = veh.timestep_time
            plt.plot( lanePosX,lanePosY, '.')
            plt.plot( vehX,vehY, 'o')  # 蓝色圆点实线 
            plt.show()
        

    break
    
plt.show()


#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()

