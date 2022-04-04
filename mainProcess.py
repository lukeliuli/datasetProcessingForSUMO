import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('vanet-trace-creteil-20130924-0700-0900.csv',sep = ';')
print("#################################################################")
print("df.head()\n",df.head())
#print("df.info()\n",df.info())
#print(df.describe())
veh_lane1 = df[df.vehicle_lane=='-1356_0']
print("#################################################################")
print("veh_lane1\n",veh_lane1)

veh_lane = df.vehicle_lane
print("#################################################################")
print("veh_lane.unique()\n",veh_lane.unique())
print("#################################################################")

for i,data in enumerate(veh_lane.unique()):
    #print(i,data)
    vehInOneLane = df[df.vehicle_lane==data]
    #print(vehInOneLane)
    lanePosX =  vehInOneLane.vehicle_x
    lanePosY =  vehInOneLane.vehicle_y
    #print(lanePosX)
    plt.plot( lanePosX,lanePosY, '.')  # 蓝色圆点实线
    
plt.show()


#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()