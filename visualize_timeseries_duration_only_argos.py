# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:36:10 2019

@author: pengrui
"""
import matplotlib.dates as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import glob
import time
import csv

csv_list = glob.glob('/content/drive/My Drive/*_summary.csv')  # search csv files in current folder
print('%s csvfiles searched in total'% len(csv_list))
print('processing............')
fig=plt.figure(figsize=(15,15))
color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']
p=0
k=0
for i in csv_list: #i is a filename which is processed
    df = pd.read_csv(i)
    ptt = df['PTT']
    track1=df['argos_track']
    start1 = df['argos_start_date']
    end1 = df['argos_end_date']
    track2=df['gps_track']
    start2 = df['gps_start_date']
    end2 = df['gps_end_date']
    for j in df.index:
        s = datetime.strptime(start1[j], '%Y-%m-%d %H:%M:%S').date()
        e = datetime.strptime(end1[j], '%Y-%m-%d %H:%M:%S').date()
        ss = dt.date2num(s)
        ee = dt.date2num(e)
        '''
        s2 = datetime.strptime(start2[j], '%Y-%m-%d %H:%M:%S').date()
        e2 = datetime.strptime(end2[j], '%Y-%m-%d %H:%M:%S').date()
        ss2 = dt.date2num(s2)
        ee2 = dt.date2num(e2)
        '''        
        plt.plot([ss,ee],[j+p,j+p], marker = ".",color=color[k])
        #plt.plot([ss2,ee2],[j-0.15,j-0.15],marker = ".",linestyle='--',color=color[k])
    a=csv_list[k].find('_')
    plt.text(ss,j+0.1+p,csv_list[k][24:a],size=14,color=color[k])       
    k+=1
    p+=0.2
ax = plt.gca()
formatter = dt.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(formatter)
#ax.xaxis.grid(True)  
#ax.yaxis.grid(True)
firstdays=dt.MonthLocator() # Get data for the first day of the month
locate=dt.MonthLocator(range(1, 13), bymonthday=1, interval=12) # Get data on the first day of every 6 months
ax.xaxis.set_major_locator(locate) # Set the main scale
ax.xaxis.set_minor_locator(firstdays) # Set minor scale
plt.yticks([-1,26],['',''])
fig.autofmt_xdate() # Auto rotate xlabel 
plt.tick_params(axis='y', which='both', labelright='on')
plt.title('time_series_duration_only_argos')
plt.savefig('visualize_timeseries_duration_only_argos.png',dpi=200)
print('Finish！')
