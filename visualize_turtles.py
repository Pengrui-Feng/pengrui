# -*- coding: utf-8 -*-
"""
Created on Tue May  2 11:40:28 2017
comparision
@author: yifan modified by pengrui,xiaoxu
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
#from turtleModule import str2ndlist
#################################################################
path = '/home/zdong/PENGRUI/data_process/'
start_time = datetime(2017,5,8) #start of time
end_time = datetime(2019,5,1)   # end of time we want
color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']


obsData = pd.read_csv(path + 'combined_td_gps.csv') # has both observed and modeled profiles
#tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsturtle_id=obsData['PTT']
ids = obsturtle_id.unique() # this is the interest turtle id


Time = obsData['argos_date']))
indx=np.where((Time>=start_time) & (Time<end_time))[0]
time=Time[indx]
time.sort()


Data = obsData.ix[time.index]
Data.index=range(len(indx))
obsTime = Data['argos_date']
obsTemp = Data['temp']
obsDepth = Data['depth']
obsIDs = Data['PTT']
obsID=obsIDs.unique()
for i in obsID:
  if i not in ids:
      print (i)
mintime=obsTime[0].strftime('%m-%d-%Y')
maxtime=obsTime[len(obsTime)-1].strftime('%m-%d-%Y')
'''
data=pd.DataFrame()
data['turtle_id']=Data['PTT']
data['Time']=Data['END_DATE']
data['Lat']=Data['lat']
data['Lon']=Data['lon']
data['Depth']=Data['TEMP_DBAR']
data['Temperature']=Data['TEMP_VALS']
data.to_csv(path+'each_data/data(%s~%s).csv'%(mintime,maxtime))
'''
month,day=[],[]
for d in obsTime.index:
    day.append(obsTime[d].day)
    month.append(obsTime[d].month)    

shift = 4
maxdepth = 60

#
m=int(len(Data)/2)
fig=plt.figure()
ax1=fig.add_subplot(2,1,1)
for j in range(0,m):
    for i in range(len(ids)):       
        if obsID[j]==ids[i]:  # to give the different color line for each turtle
            ax1.plot(np.array(obsTemp[j])+shift*j,obsDepth[j],color=color[i],linewidth=1)#,label='id:'+str(obsID[j])
            if obsDepth[j][-1]< maxdepth:
                ax1.text(obsTemp[j][-1]+shift*j-2,obsDepth[j][-1]+1,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            else:
                ax1.text(obsTemp[j][-1]+shift*j-2,60,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            ax1.set_ylim([maxdepth,-1])
            plt.setp(ax1.get_xticklabels() ,visible=False)
ax2=fig.add_subplot(2,1,2)
for j in range(m,len(Data)):
    for i in range(len(ids)):
        if obsID[j]==ids[i]:  # to give the different color line for each turtle
            ax2.plot(np.array(obsTemp[j])+shift*j,obsDepth[j],color=color[i],linewidth=1)#,label='id:'+str(obsID[j])
            if obsDepth[j][-1] < maxdepth:
                ax2.text(obsTemp[j][-1]+shift*j-2,obsDepth[j][-1]+1,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            else:
                ax2.text(obsTemp[j][-1]+shift*j-2,60,str(month[j])+'/'+str(day[j]),color='r',fontsize=5)
            ax2.set_ylim([maxdepth,-1])
            plt.setp(ax2.get_xticklabels() ,visible=False)

middletime=obsTime[m].strftime('%m-%d-%Y')        
ax1.set_title('profiles color-coded-by-turtle( '+mintime+'~'+middletime+' )')#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
ax2.set_title('( '+middletime+'~'+maxtime+' )')
fig.text(0.5, 0.04, 'Temperature by time('+shift+' degree offset)', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)

plt.savefig(path+'turtle_comparison/turtle_comparison(%s~%s).png'%(mintime,maxtime),dpi=200)#put the picture to the file"turtle_comparison"
plt.show()

for i in range(len(obsID)):
    e=obsID[i]
    indx=[]  
    for i in Data.index:
        if obsIDs[i]==e:   
            indx.append(i)
    Data_e = Data.ix[indx]  
    Data_e.index= range(len(indx))             
    Time_e= pd.Series((datetime.strptime(x, '%m/%d/%Y %H:%M') for x in Data_e['END_DATE']))
    Temp_e = pd.Series(str2ndlist(Data_e['TEMP_VALS']))
    Depth_e = pd.Series(str2ndlist(Data_e['TEMP_DBAR']))
    
    fig=plt.figure()
    ax1=fig.add_subplot(1,1,1)
    l=len(Data_e)/40.0
    for j in Data_e.index:
        
        for c in range(len(ids)):
            if e==ids[c]:
               ax1.plot(np.array(Temp_e[j])+4*j,Depth_e[j],color=color[c],linewidth=1)
        if Depth_e[j][-1]<maxdepth:
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
