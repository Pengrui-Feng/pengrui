# -*- coding: utf-8 -*-
"""
Modified on Nov  6 11:40:28 2019
plot profile of each turtle and all turtles during selected days, map each turtle dive location
@author: yifan modified by pengrui,xiaoxu
"""
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pandas as pd
from datetime import datetime, timedelta
from turtleModule import draw_basemap

##### SET basic parameters
path = '/home/zdong/PENGRUI/data_process/'
start_time = datetime(2017,5,8) #start of time
end_time = datetime(2018,5,1)   # end of time we want
lonsize = [-76.8, -69.8]
latsize = [34.9, 41.5]

color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']

##### read in csv file and creat DataFrame
obsData = pd.read_csv(path + 'combined_td_gps.csv') # has both observed and modeled profiles
obsturtle_id=obsData['PTT']
ids = obsturtle_id.unique() # this is the interest turtle id

Time = pd.Series((datetime.strptime(x, '%m/%d/%Y %H:%M') for x in obsData['argos_date']))
indx=np.where((Time >= start_time) & (Time < end_time))[0]
time=Time[indx]
time.sort()

Data = obsData.ix[time.index]
Data.index=range(len(indx))
obsTime = pd.Series((datetime.strptime(x, '%m/%d/%Y %H:%M') for x in Data['END_DATE']))
obsTemp = pd.Series(Data['temp'])
obsDepth = pd.Series(Data['depth'])
obsIDs = Data['PTT']
dives = Data['dive_num']
obsID=obsIDs.unique()

mintime=obsTime[0].strftime('%m-%d-%Y')
maxtime=obsTime[len(obsTime)-1].strftime('%m-%d-%Y')


##### Profiles with each PTT temp VS depth
shift = 2
maxdepth = 60

m=int(len(Data)/2)
fig=plt.figure()
ax1=fig.add_subplot(2,1,1)
for j in range(0,m):
    for i in range(len(ids)):       
        for k in range(len(dives.unique())):
            if obsID[j]==ids[i]:  # to give the different color line for each turtle
                ax1.plot(np.array(obsTemp[j])+shift*j,obsDepth[j],color=color[i],linewidth=1)
                if obsDepth[j][-1] < maxdepth:
                    ax1.text(obsTemp[j][-1]+shift*j-2,obsDepth[j][-1]+1,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
                else:
                    ax1.text(obsTemp[j][-1]+shift*j-2,60,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
                ax1.set_ylim([maxdepth,-1])
                plt.setp(ax1.get_xticklabels() ,visible=False)

ax2=fig.add_subplot(2,1,2)
for j in range(m,len(Data)):
    for i in range(len(ids)):
        for k in range(len(dives.unique())):
            if obsID[j]==ids[i]:  # to give the different color line for each turtle
                ax1.plot(np.array(obsTemp[j])+shift*j,obsDepth[j],color=color[i],linewidth=1)#,label='id:'+str(obsID[j])
                if obsDepth[j][-1] < maxdepth:
                    ax1.text(obsTemp[j][-1]+shift*j-2,obsDepth[j][-1]+1,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
                else:
                    ax1.text(obsTemp[j][-1]+shift*j-2,60,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
                ax1.set_ylim([maxdepth,-1])
                plt.setp(ax1.get_xticklabels() ,visible=False)

middletime=obsTime[m].strftime('%m-%d-%Y')        
ax1.set_title('profiles color-coded-by-turtle( '+mintime+'~'+middletime+' )')
ax2.set_title('( '+middletime+'~'+maxtime+' )')
fig.text(0.5, 0.04, 'Temperature by time('+shift+' degree offset)', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)

plt.savefig(path+'turtle_comparison/turtle_comparison(%s~%s).png'%(mintime,maxtime),dpi=200)
plt.show()

##### Profiles with all turtles during the specific days
for i in range(len(obsID)):
    e=obsID[i]
    indx=[]  
    for i in Data.index:
        if obsIDs[i]==e:   
            indx.append(i)
    Data_e = Data.ix[indx]  
    Data_e.index= range(len(indx))             
    Time_e= pd.Series((datetime.strptime(x, '%m/%d/%Y %H:%M') for x in Data_e['END_DATE']))
    Temp_e = pd.Series(Data_e['temp'])
    Depth_e = pd.Series(Data_e['depth'])
    
    fig=plt.figure()
    ax1=fig.add_subplot(1,1,1)
    l=len(Data_e)/40.0
    for j in Data_e.index:
        for c in range(len(ids)):
            if e==ids[c]:
               ax1.plot(np.array(Temp_e[j])+4*j,Depth_e[j],color=color[c],linewidth=1)
        if Depth_e[j][-1] < maxdepth:
            ax1.text(Temp_e[j][-1]+shift*j-l,Depth_e[j][-1]+2,round(Temp_e[j][-1],1),color='r',fontsize=6)
        else:
            ax1.text(Temp_e[j][-1]+shift*j-l,60,round(Temp_e[j][-1],1),color='r',fontsize=6)
        if j%2==0:
            ax1.text(Temp_e[j][0]+shift*j-l,Depth_e[j][0],round(Temp_e[j][0],1),color='k',fontsize=5)
        else:
            ax1.text(Temp_e[j][0]+shift*j-l,Depth_e[j][0]-1,round(Temp_e[j][0],1),color='k',fontsize=5)
    ax1.set_ylim([maxdepth,-1])
        #plt.setp(ax1.get_xticklabels() ,visible=False)
    ax1.set_xticks([int(Temp_e[0][-1]), int(Temp_e[0][-1])+4])
        #ax1.set_xticklabels(['a', 'b', 'c'])
    mintime_e=Time_e[0].strftime('%m-%d-%Y')
    maxtime_e=Time_e[len(Time_e)-1].strftime('%m-%d-%Y')
    if len(Data_e)==1:
        fig.text(0.5, 0.04, 'Temperature ('+u'°C'+')', ha='center', va='center', fontsize=14)
    else:
        fig.text(0.5, 0.04, 'Temperature (each profile offset by '+shift+'°C)', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
    
    if mintime_e==maxtime_e:
        ax1.set_title(str(e) +'_profiles( '+mintime_e+' )')
        
    else:
        ax1.set_title(str(e) +'_profiles( '+mintime_e+'~'+maxtime_e+' )')#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
    fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)
    plt.savefig(path+'each_profiles/%s~%s/%s_profiles(%s~%s).png'% (mintime,maxtime,e,mintime,maxtime),dpi=200)#put the picture to the file "each_profiles"
    plt.show()

##### Map each turtle dive location
weeks=11# the number means how many weeks should plot from the one exact days
for j in range(weeks):
    start_time=(datetime(start_time)+timedelta(days=j*7)).strftime('%m-%d-%Y')
    end_time=(datetime(end_time)+timedelta(days=j*7+6)).strftime('%m-%d-%Y')
    obsData = pd.read_csv('each_data/data(%s~%s).csv'%(start_time,end_time)) # has both observed and modeled profiles
    obsLat=obsData['Lat']
    obsLon=obsData['Lon']
    
    waterData=pd.read_csv('/home/zdong/PENGRUI/get_original_data/tu102_ctd.csv')
    wd=waterData['MAX_DBAR'].dropna()
    Lat=waterData['lat'].dropna()
    Lon=waterData['lon'].dropna()
    
    fig =plt.figure()
    ax = fig.add_subplot(111)
    for j in range(len(ids)):
        indx=[]  # this indx is to get the specifical turtle all index in obsData ,if we use the "where" function ,we just get the length  of tf_index.
        for i in obsData.index:
            if obsturtle_id[i]==ids[j]:   
                indx.append(i)
        Time = obsTime[indx]
        lat = obsLat[indx]
        lon = obsLon[indx]
        for i in range(len(ids)): 
            if ids[j]==ids[i]:
               plt.plot(lon, lat,linestyle='-',marker='o',markersize=3,linewidth=1,color=color[i],label='id:'+str(ids[j]))  #  
    draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2)    
    
    lon_is = np.linspace(lonsize[0],lonsize[1],150)
    lat_is = np.linspace(latsize[0],latsize[1],150)  #use for depth line
    depth_i=griddata(np.array(Lon),np.array(Lat),np.array(wd),lon_is,lat_is,interp='linear')
    cs=plt.contour(lon_is, lat_is,depth_i,levels=[100],colors = 'r',linewidths=1,linestyles='--')  #plot 100m depth
    ax.annotate('100m water depth',color='r',fontsize=6,xy=(-73.2089,38.905),xytext=(-73.3034,38.5042),arrowprops=dict(color='red',arrowstyle="->",
                                connectionstyle="arc3"))#xy=(-73.5089,38.505),xytext=(-73.7034,38.0042)
    mintime=obsTime[0].strftime('%m-%d-%Y')
    maxtime=obsTime[len(obsTime)-1].strftime('%m-%d-%Y')
    plt.title('turtle position( '+mintime+'~'+maxtime+' )')#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
    plt.legend(loc='lower right',ncol=2,fontsize = 'xx-small')
    #plt.savefig('turtle_comparison(%s~%s).png'%(mintime,maxtime),dpi=200)
    plt.savefig('map/map(%s~%s).png'%(mintime,maxtime),dpi=200)
plt.show()
