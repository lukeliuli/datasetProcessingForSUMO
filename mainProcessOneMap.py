import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib
from matplotlib.animation import FFMpegWriter

#matplotlib.use("Agg")
#print(FFMpegWriter.bin_path())

df = pd.read_csv('.\data\data1.csv',sep = ';')
print("#################################################################")
print("df.head()\n",df.head())
#print("df.info()\n",df.info())
#print(df.describe())




print("#################################################################")
print("显示轨迹")
print("#################################################################")


fg1= plt.figure(figsize=(8,5))
metadata = dict(title='france Dataset traces', artist='lukeliuli',comment='france Dataset traces')
writer = FFMpegWriter(fps=5, metadata=metadata)
writer.setup(fg1, "1.mp4", dpi=600)

mapPosX =  df.vehicle_x
mapPosY =  df.vehicle_y
plt.plot(mapPosX,mapPosY, '.',color = 'black',linewidth=1,markersize=0.3,label='lane')


vehsInOneMap =df.sort_values(by='timestep_time',ascending=True)


#提取时刻
timeList = vehsInOneMap.timestep_time.unique()
for t in timeList:#枚举每个时间
    title ="Time:"+str(t)+";"
    print(title)

    vehsAtTime = vehsInOneMap[vehsInOneMap.timestep_time == float(t)] 
    plt.plot(mapPosX,mapPosY, '.',color = 'black',linewidth=1,markersize=0.3,label='lane')

    for index, veh in vehsAtTime.iterrows():#每一辆车
        #print(index,veh)
        vehX =  veh.vehicle_x
        vehY =  veh.vehicle_y
        vehVel = veh.vehicle_speed
        vehTime  = veh.timestep_time
        vehID = veh.vehicle_id
        
        #title = title+"\n"+vehID+",Speed:"+str(vehVel)+";"
    
        randNum =sum([ord(x) for x in str(vehID)])
        colorList= ['r', 'g', 'b', 'y', 'c', 'm', 'k']
        plt.plot( vehX,vehY, 'o',color= colorList[randNum%7])  # 蓝色圆点实线 
        #plt.annotate(str(vehVel),xy=(vehX, vehY),  xytext=(-50, 10), textcoords='offset points') 
    
        

    plt.title(title,fontsize='large')    
    #plt.show()
    writer.grab_frame()
    #plt.ioff()
    plt.cla()
writer.finish()
    
    
    




#plt.plot(df.vehicle_x,df.vehicle_y, '.')  # 蓝色圆点实线
#plt.show()

