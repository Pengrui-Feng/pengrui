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

csv_list = glob.glob('/content/drive/My Drive/PENGRUI/summary/*_Summary.csv')  # search csv files in current folder
print('%s csvfiles searched in total'% len(csv_list))
print('processing............')
fig =plt.figure(figsize=(15,10))
color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']

k=0
for i in csv_list: #i is a filename which is processed
    df = pd.read_csv(i)
    ptt = df['PTT']
    tracks=df['length_of_track']
    start = df['start_date']
    end = df['end_date']
    for j in df.index:
        s = datetime.strptime(start[j], '%Y-%m-%d %H:%M:%S').date()
        e = datetime.strptime(end[j], '%Y-%m-%d %H:%M:%S').date()
        ss = dt.date2num(s)
        ee = dt.date2num(e)
        plt.plot([ss,ee],[j,j], marker = ".",color=color[k])
    a=csv_list[k].find('_')
    plt.text(ss,j+0.3,csv_list[k][40:a],size=14,color=color[k])       
    k+=1

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
plt.title('database_duration_comparison')
plt.savefig('visualize_db_duration.png',dpi=200)
print('Finish！')
