# -*- coding: utf-8 -*-
"""
Modified by JiM and Pengrui in Nov 2019
plot all turtles during selected days and profile of each turtle, map each turtle dive location
@author: yifan
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from matplotlib.mlab import griddata # no longer available in Python 3
#from scipy.interpolate import griddata # in python 3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from turtleModule import str2ndlist
from mpl_toolkits.basemap import Basemap
from turtleModule import draw_basemap

##### SET basic parameters
start_time = datetime(2018,7,25).strftime('%m-%d-%Y') 
end_time = datetime(2018,7,31).strftime('%m-%d-%Y')   # create a forder named by 'IOError'
lonsize = [-76.8, -69.8]
latsize = [34.9, 41.5]
color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']
shift = 4 # offset of profiles in degC
maxdepth = 60 # maximum depth of profile plot
t_ids=[161291, 161292, 161296, 172191, 175934, 175935, 161295, 175939,161299, 161303, 161294, 161297, 161298, 161300, 161301, 161304,172179, 172188, 175938, 175932, 175936, 175940]
#
obsData = pd.read_csv('merge_td_gps.csv') # has both observed and modeled profiles
obsturtle_id=obsData['PTT']
ids=obsturtle_id.unique()#118905 # this is the interest turtle id

Time = pd.Series((datetime.strptime(x, '%m/%d/%y %H:%M:%S') for x in obsData['END_DATE']))
#indx=np.where((Time>=end_time-timedelta(days=7)) & (Time<end_time))[0]
indx=np.where((Time>=start_time) & (Time<=end_time))[0]
time=Time[indx]
time.sort()

Data = obsData.ix[time.index]
Data.index=range(len(indx))
obsTime =  pd.Series((datetime.strptime(x, '%m/%d/%y %H:%M:%S') for x in Data['END_DATE']))
obsTemp = pd.Series(str2ndlist(Data['TEMP_VALS']))
obsDepth = pd.Series(str2ndlist(Data['TEMP_DBAR']))
obsID = Data['PTT']
obsIDs=obsID.unique()
for i in obsIDs:
  if i not in t_ids:
      print i
mintime=obsTime[0].strftime('%m-%d-%Y')
maxtime=obsTime[len(obsTime)-1].strftime('%m-%d-%Y')

data=pd.DataFrame()
data['turtle_id']=Data['PTT']
data['Time']=Data['END_DATE']
data['Lat']=Data['lat']
data['Lon']=Data['lon']
data['Depth']=Data['TEMP_DBAR']
data['Temperature']=Data['TEMP_VALS']
data.to_csv('period_turtles_data/data_%s~%s.csv'%(mintime,maxtime))

month,day=[],[]
for d in obsTime.index:
    day.append(obsTime[d].day)
    month.append(obsTime[d].month)    

#####  plot all turtles during selected days          
m=int(len(Data)/2)
fig=plt.figure()
ax1=fig.add_subplot(2,1,1)
for j in range(0,m):
    for i in range(len(t_ids)):       
        if obsID[j]==t_ids[i]:  # to give the different color line for each turtle
            ax1.plot(np.array(obsTemp[j])+shift*j,obsDepth[j],color=color[i],linewidth=1)#,label='id:'+str(obsID[j])
            if obsDepth[j][-1]<maxdepth:
                ax1.text(obsTemp[j][-1]+shift*j-2,obsDepth[j][-1]+1,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            else:
                ax1.text(obsTemp[j][-1]+shift*j-2,maxdepth,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            ax1.set_ylim([maxdepth,-1])
            plt.setp(ax1.get_xticklabels() ,visible=False)
ax2=fig.add_subplot(2,1,2)
for j in range(m,len(Data)):
    for i in range(len(t_ids)):       
        if obsID[j]==t_ids[i]:  # to give the different color line for each turtle
            ax2.plot(np.array(obsTemp[j])+shift*j,obsDepth[j],color=color[i],linewidth=1)#,label='id:'+str(obsID[j])
            if obsDepth[j][-1]<maxdepth:
                ax2.text(obsTemp[j][-1]+shift*j-2,obsDepth[j][-1]+1,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            else:
                ax2.text(obsTemp[j][-1]+shift*j-2,maxdepth,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            ax2.set_ylim([maxdepth,-1])
            plt.setp(ax2.get_xticklabels() ,visible=False)
middletime=obsTime[m].strftime('%m-%d-%Y')        
ax1.set_title('profiles color-coded-by-turtle during '+mintime+' ~ '+middletime )#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
ax2.set_title(middletime+' ~ '+maxtime)
fig.text(0.5, 0.04, 'Temperature by time'+str(shift)+' degree offset', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)

plt.savefig('period_turtles_profile/profile_%s~%s.png'%(mintime,maxtime),dpi=200)#put the picture to the file"turtle_comparison"
plt.show()

##### plot profile of each turtle
for i in range(len(obsIDs)):
    e=obsIDs[i]
    indx=[]  
    for i in Data.index:
        if obsID[i]==e:   
            indx.append(i)
    Data_e = Data.ix[indx]  
    Data_e.index= range(len(indx))             
    Time_e= pd.Series((datetime.strptime(x, '%m/%d/%y %H:%M:%S') for x in Data_e['END_DATE']))
    Temp_e = pd.Series(str2ndlist(Data_e['TEMP_VALS']))
    Depth_e = pd.Series(str2ndlist(Data_e['TEMP_DBAR']))
    
    fig=plt.figure()
    ax1=fig.add_subplot(1,1,1)
    l=len(Data_e)/40.0
    for j in Data_e.index:
        
        for c in range(len(t_ids)):
            if e==t_ids[c]:
               ax1.plot(np.array(Temp_e[j])+shift*j,Depth_e[j],color=color[c],linewidth=1)
        if Depth_e[j][-1]<maxdepth:
            ax1.text(Temp_e[j][-1]+shift*j-l,Depth_e[j][-1]+2,round(Temp_e[j][-1],1),color='r',fontsize=6)
        else:
            ax1.text(Temp_e[j][-1]+shift*j-l,maxdepth,round(Temp_e[j][-1],1),color='r',fontsize=6)
        if j%2==0:
            ax1.text(Temp_e[j][0]+shift*j-l,Depth_e[j][0],round(Temp_e[j][0],1),color='k',fontsize=5)
        else:
            ax1.text(Temp_e[j][0]+shift*j-l,Depth_e[j][0]-1,round(Temp_e[j][0],1),color='k',fontsize=5)
    ax1.set_ylim([maxdepth,-1])
        #plt.setp(ax1.get_xticklabels() ,visible=False)
    ax1.set_xticks([int(Temp_e[0][-1]), int(Temp_e[0][-1])+shift])
        #ax1.set_xticklabels(['a', 'b', 'c'])
    mintime_e=Time_e[0].strftime('%m-%d-%Y')
    maxtime_e=Time_e[len(Time_e)-1].strftime('%m-%d-%Y')
    if len(Data_e)==1:
        fig.text(0.5, 0.04, 'Temperature '+'°C', ha='center', va='center', fontsize=14)
    else:
        fig.text(0.5, 0.04, 'Temperature_each profile offset by'+str(shift)+'°C', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
    
    if mintime_e==maxtime_e:
        ax1.set_title(str(e) +'_profiles '+mintime_e+' ')
        
    else:
        ax1.set_title(str(e) +'_profiles '+mintime_e+'~'+maxtime_e+' ')#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
    fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)
    plt.savefig('per_turtle_period/%s~%s/%s_profiles_%s~%s.png'% (mintime,maxtime,e,mintime,maxtime),dpi=200)#put the picture to the file "each_profiles"
    plt.show()


##### Map
#weeks=1  # the number means how many weeks should plot from the one exact days
#for j in range(weeks):# 
    #start_time=(datetime(2018,7,25)+timedelta(days=j*7)).strftime('%m-%d-%Y')
    #endtime=(datetime(2018,7,25)+timedelta(days=j*7+6)).strftime('%m-%d-%Y')
obsdata = pd.read_csv('period_turtles_data/data_%s~%s.csv'%(start_time,end_time)) # has both observed and modeled profiles
obstime =  pd.Series((datetime.strptime(x, '%m/%d/%y %H:%M:%S') for x in obsdata['Time']))
obsLat=obsdata['Lat']
obsLon=obsdata['Lon']
obsturtle_id=obsdata['turtle_id']
ids=obsturtle_id.unique() # this is the interest turtle id
    
waterData=pd.read_csv('tu94_depthbottom.csv')
wd=waterData['depth_bottom'].dropna()
Lat=waterData['lat'].dropna()
Lon=waterData['lon'].dropna()
    
fig =plt.figure()
ax = fig.add_subplot(111)
for j in range(len(ids)):
    indx=[]  # this indx is to get the specifical turtle all index in obsData ,if we use the "where" function ,we just get the length  of tf_index.
    for i in obsdata.index:
        if obsturtle_id[i]==ids[j]:   
            indx.append(i)
    Time = obstime[indx]
    lat = obsLat[indx]
    lon = obsLon[indx]
    for i in range(len(t_ids)): 
        if ids[j]==t_ids[i]:
            plt.plot(lon, lat,linestyle='-',marker='o',markersize=3,linewidth=1,color=color[i],label='id:'+str(ids[j]))  #  
draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2)    
    
lon_is = np.linspace(lonsize[0],lonsize[1],150)
lat_is = np.linspace(latsize[0],latsize[1],150)  #use for depth line
depth_i=griddata(np.array(Lon),np.array(Lat),np.array(wd),lon_is,lat_is)#,interp='linear')
cs=plt.contour(lon_is, lat_is,depth_i,levels=[100],colors = 'r',linewidths=1,linestyles='--')  #plot 100m depth
ax.annotate('100m water depth',color='r',fontsize=6,xy=(-73.2089,38.905),xytext=(-73.3034,38.5042),arrowprops=dict(color='red',arrowstyle="->",
                                connectionstyle="arc3"))#xy=(-73.5089,38.505),xytext=(-73.7034,38.0042)
#mintime=obsTime[0].strftime('%m-%d-%Y')
#maxtime=obsTime[len(obsTime)-1].strftime('%m-%d-%Y')
plt.title('turtle position '+mintime+'~'+maxtime+' ')#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
plt.legend(loc='lower right',ncol=2,fontsize = 'x-small')
plt.savefig('map/map_%s~%s.png'%(mintime,maxtime),dpi=200)
plt.show()

