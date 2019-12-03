# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:42:22 2019

@author: pengrui
"""

import matplotlib.dates as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter, MONDAY, MonthLocator, YearLocator

path1='/home/zdong/PENGRUI/summary/'
path2='/home/zdong/PENGRUI/summary/'

df = pd.read_csv(path1+'Summary_tu99.csv')
ptt = df['PTT']
tracks=df['length_of_track']
start = df['start_date']
end = df['end_date']

fig =plt.figure()
for i in df.index:
    s = datetime.strptime(start[i], '%Y-%m-%d %H:%M:%S').date()
    e = datetime.strptime(end[i], '%Y-%m-%d %H:%M:%S').date()
    ss = dt.date2num(s)
    ee = dt.date2num(e)
    plt.plot([ss,ee],[i,i], marker = ".")
    #plt.text(ss,i,tracks[i],size=10)
ax = plt.gca()
formatter = DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(formatter)
ax.grid(True)  
firstdays=MonthLocator() # Get data for the first day of the month
locate=MonthLocator(range(1, 13), bymonthday=1, interval=3) # Get data on the first day of every 3 months

ax.xaxis.set_major_locator(locate) # Set the main scale
ax.xaxis.set_minor_locator(firstdays) # Set minor scale

fig.autofmt_xdate() # Auto rotate xlabel
plt.tick_params(axis='y', which='both', labelright='on') # 

#plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],['PTT','161291','161292','161296','172191','175934','175935','161295','175939','161299','161303','161294','161297','161298','161300','161301','161304','172179','172188','175938','175932','175936','175940'])#tu102
plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['PTT','161426','161427','161428','161432','161433','161435','161429','161436','161437','161430','161434','161439','161431','161438','161440'])#tu99
plt.title('tu99_ptt-date')
plt.savefig(path2+'tu99_ptt-date.png',dpi=200)
plt.show()
